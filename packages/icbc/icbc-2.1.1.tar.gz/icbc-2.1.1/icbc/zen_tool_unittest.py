import unittest
import zen_tool as z



class TestZ(unittest.TestCase):
    def test_base64(self):
        a="source"
        b=z.base64_encode(a,6)
        self.assertEqual(z.base64_encode(a,6),"VmpGb2QxTnJOVlpOVm1oVllteEtWbGxzYUdwUFVUMDk=")
        self.assertEqual(z.base64_decode("VmpGb2QxTnJOVlpOVm1oVllteEtWbGxzYUdwUFVUMDk=",6),a)
    def test_encode(self):
        a=z.encode("test","key")
        self.assertEqual(a,"==dGVzdA")
        b=z.decode(a,"key")
        self.assertEqual(b,"test")
        c=z.decode(a,"ke")
        self.assertEqual(c,None)
    def test_md5(self):
        self.assertEqual(z.md5("test"),"098f6bcd4621d373cade4e832627b4f6")
unittest.main()
