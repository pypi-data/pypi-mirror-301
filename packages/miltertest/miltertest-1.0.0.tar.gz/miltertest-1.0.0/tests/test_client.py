# Copyright 2011 Chris Siebenmann
# Copyright 2024 Paul Arthur MacIain
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import unittest

from miltertest import codec
from miltertest import constants
from miltertest import (
    MilterConnection,
    MilterError,
)


class ConvError(Exception):
    pass


# ---
# test infrastructure

# These are from the perspective of the socket; it expects you to read
# or write.
READ, WRITE = object(), object()


# A fake socket object that implements .recv() and .sendall().
# It is fed a conversation that it expects (a sequence of read and
# write operations), and then verifies that the sequence that happens
# is what you told it to expect.
# Because this is specific to verifying the milter conversation, it
# does not bother having to know exactly what the written messages are;
# for our purpose, it is enough to know their type.
# (Optionally it can also know the result dictionary and verify it,
# because that turned out to be necessary.)
class FakeSocket:
    def __init__(self, conv=None):
        if conv is None:
            conv = []
        self.conv = conv
        self.cindex = 0

    # verify that a .recv() or .sendall() is proper, ie that it
    # is the next expected action.
    def _verify_conv(self, adir):
        if self.cindex >= len(self.conv):
            raise ConvError('unexpected action')
        if adir != self.conv[self.cindex][0]:
            raise ConvError('sequence mismatch')

    def _add(self, adir, what):
        self.conv.append((adir, what))

    def addReadMsg(self, cmd, **args):
        """Add a message to be read; arguments are as per
        encode_msg."""
        self._add(READ, codec.encode_msg(cmd, **args))

    def addRead(self, buf):
        """Add a raw string to be read."""
        self._add(READ, buf)

    def addWrite(self, cmd):
        """Add an expected write command."""
        self._add(WRITE, (cmd,))

    def addFullWrite(self, cmd, **args):
        """Add an expected write command and its full parameters."""
        self._add(WRITE, (cmd, args))

    def addMTAWrite(self, cmd):
        """Add an expected write command and then an SMFIR_CONTINUE
        reply to it."""
        self._add(WRITE, (cmd,))
        self.addReadMsg(constants.SMFIR_CONTINUE)

    def isEmpty(self):
        """Returns whether or not all expected reads and writes
        have been consumed."""
        return self.cindex == len(self.conv)

    #
    # The actual socket routines we emulate.
    def recv(self, nbytes):
        self._verify_conv(READ)
        # nbytes should be at least as large as what we are
        # scheduled to send.
        _, obj = self.conv[self.cindex]
        self.cindex += 1
        if isinstance(obj, (list, tuple)):
            obj = codec.encode_msg(obj[0], **obj[1])
        if len(obj) > nbytes:
            raise ConvError('short read')
        return obj

    def sendall(self, buf):
        self._verify_conv(WRITE)
        # We verify that we got the right sort of stuff
        r = codec.decode_msg(buf)
        _, wres = self.conv[self.cindex]
        self.cindex += 1
        otype = wres[0]
        if r[0] != otype:
            raise ConvError(f'Received unexpected reply {r[0]} instead of {otype}')
        if len(wres) > 1 and r[1] != wres[1]:
            raise ConvError(f'Unexpected reply parameters: {r[1]} instead of {wres[1]}')


# -----
#
class basicTests(unittest.TestCase):
    def testShortReads(self):
        """Test that we correctly read multiple times to reassemble
        a short message, and that we get the right answer."""
        ams = constants.SMFIC_CONNECT
        adict = {'hostname': 'localhost', 'family': '4', 'port': 1678, 'address': '127.10.10.1'}
        msg = codec.encode_msg(ams, **adict)
        msg1, msg2 = msg[:10], msg[10:]
        s = FakeSocket()
        s.addRead(msg1)
        s.addRead(msg2)

        mbuf = MilterConnection(s)
        rcmd, rdict = mbuf._recv()
        self.assertEqual(ams, rcmd)
        self.assertEqual(adict, rdict)
        self.assertTrue(s.isEmpty())

    def testProgressReads(self):
        """Test that we correctly read multiple progress messages
        before getting the real one."""
        s = FakeSocket()
        s.addReadMsg(constants.SMFIR_PROGRESS)
        s.addReadMsg(constants.SMFIR_PROGRESS)
        s.addReadMsg(constants.SMFIR_PROGRESS)
        s.addReadMsg(
            constants.SMFIR_DELRCPT,
            rcpt=[
                '<a@b.c>',
            ],
        )
        mbuf = MilterConnection(s)
        rcmd, rdict = mbuf.recv()
        self.assertEqual(rcmd, constants.SMFIR_DELRCPT)
        self.assertTrue(s.isEmpty())


class continuedTests(unittest.TestCase):
    def testHeaders(self):
        """Test that we handle writing a sequence of headers in
        the way that we expect."""
        s = FakeSocket()
        hdrs = (('From', 'Chris'), ('To', 'Simon'), ('Subject', 'Yak'))
        for _ in hdrs:
            s.addMTAWrite(constants.SMFIC_HEADER)
        mbuf = MilterConnection(s)
        rcmd, rdict = mbuf.send_headers(hdrs)
        self.assertEqual(rcmd, constants.SMFIR_CONTINUE)
        self.assertTrue(s.isEmpty())

    def testShortHeaders(self):
        """Test that we return early from a series of header writes
        if SMFIR_CONTINUE is not the code returned."""
        s = FakeSocket()
        hdrs = (('From', 'Chris'), ('To', 'Simon'), ('Subject', 'Yak'))
        s.addMTAWrite(constants.SMFIC_HEADER)
        s.addWrite(constants.SMFIC_HEADER)
        s.addReadMsg(constants.SMFIR_ACCEPT)
        with self.assertRaises(MilterError):
            MilterConnection(s).send_headers(hdrs)
        self.assertTrue(s.isEmpty())

    def testBodySequence(self):
        """Test that we handle writing a large body in the way
        we expect."""
        s = FakeSocket()
        body = 3 * 65535 * '*'
        s.addMTAWrite(constants.SMFIC_BODY)
        s.addMTAWrite(constants.SMFIC_BODY)
        s.addMTAWrite(constants.SMFIC_BODY)
        mbuf = MilterConnection(s)
        rcmd, rdict = mbuf.send_body(body)
        self.assertEqual(rcmd, constants.SMFIR_CONTINUE)
        self.assertTrue(s.isEmpty())

    def testShortBody(self):
        """Test that we return early from a series of body writes
        if SMFIR_CONTINUE is not the code returned."""
        s = FakeSocket()
        body = 3 * 65535 * '*'
        s.addMTAWrite(constants.SMFIC_BODY)
        s.addWrite(constants.SMFIC_BODY)
        s.addReadMsg(constants.SMFIR_ACCEPT)
        with self.assertRaises(MilterError):
            MilterConnection(s).send_body(body)
        self.assertTrue(s.isEmpty())

    optneg_mta_pairs = (
        ((constants.SMFI_V6_ACTS, constants.SMFI_V6_PROT), (constants.SMFI_V6_ACTS, constants.SMFI_V6_PROT)),
        ((constants.SMFI_V2_ACTS, constants.SMFI_V2_PROT), (constants.SMFI_V2_ACTS, constants.SMFI_V2_PROT)),
        ((0x10, 0x10), (0x10, 0x10)),
    )

    def testMTAOptneg(self):
        """Test that the MTA version of option negotiation returns
        what we expect it to."""
        for a, b in self.optneg_mta_pairs:
            s = FakeSocket()
            s.addWrite(constants.SMFIC_OPTNEG)
            s.addReadMsg(constants.SMFIC_OPTNEG, version=constants.MILTER_VERSION, actions=a[0], protocol=a[1])
            # strict=True would blow up on the last test.
            ract, rprot = MilterConnection(s).optneg_mta(strict=False)
            self.assertEqual(ract, b[0])
            self.assertEqual(rprot, b[1])

    optneg_exc_errors = (
        (constants.SMFI_V1_ACTS, 0xFFFFFF),
        (0xFFFFFF, constants.SMFI_V1_PROT),
        (0xFFFFFF, 0xFFFFFF),
    )

    def testMilterONOutside(self):
        """Test that the MTA version of option negotiation errors
        out if there are excess bits in the milter reply."""
        for act, prot in self.optneg_exc_errors:
            s = FakeSocket()
            s.addWrite(constants.SMFIC_OPTNEG)
            s.addReadMsg(constants.SMFIC_OPTNEG, version=constants.MILTER_VERSION, actions=act, protocol=prot)
            bm = MilterConnection(s)
            self.assertRaises(MilterError, bm.optneg_mta)

    optneg_milter_pairs = (
        # The basic case; MTA says all V6 actions, all V6 protocol
        # exclusions, we say we'll take all actions and we want the
        # MTA not to exclude any protocol steps.
        ((constants.SMFI_V6_ACTS, constants.SMFI_V6_PROT), (constants.SMFI_V6_ACTS, 0x0)),
        # MTA offers additional protocol exclusions, we tell it not
        # to do them but to do all V6 protocol actions.
        ((constants.SMFI_V6_ACTS, 0xFFFFFF), (constants.SMFI_V6_ACTS, 0xE00000)),
        # MTA offers additional actions, we decline.
        ((constants.SMFI_V6_ACTS, constants.SMFI_V6_PROT), (constants.SMFI_V2_ACTS, 0x00)),
    )

    def testMilterOptneg(self):
        """Test the milter version of option negotiation."""
        for a, b in self.optneg_milter_pairs:
            s = FakeSocket()
            s.addReadMsg(constants.SMFIC_OPTNEG, version=constants.MILTER_VERSION, actions=a[0], protocol=a[1])
            s.addFullWrite(constants.SMFIC_OPTNEG, version=constants.MILTER_VERSION, actions=b[0], protocol=b[1])
            ract, rprot = MilterConnection(s).optneg_milter(actions=b[0])
            self.assertEqual(ract, b[0])
            self.assertEqual(rprot, b[1])


if __name__ == '__main__':
    unittest.main()
