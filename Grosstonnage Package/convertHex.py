import binascii
import urllib2
import pprint

#f=open("GROSSTONNAGE.COM the ultimate ships database - VESSEL PAGE.htm")

#s=f.read()
def main(s):
    startIdx = s.find('<script>A4Iwrite("')+len('<script>A4Iwrite("')
    endIdx = s.find('");</script></td>')

    script = s[startIdx:endIdx]

    return urllib2.unquote(script)

if __name__ == '__main__':
    main(arg)
