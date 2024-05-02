import twitfix

tests = {
    "testTextTweet":"https://twitter.com/jack/status/20",
    "testVideoTweet":"https://twitter.com/pdxdylan/status/1540398733669666818",
    "testMediaTweet":"https://twitter.com/pdxdylan/status/1534672932106035200",
    "testMultiMediaTweet":"https://twitter.com/pdxdylan/status/1532006436703715331",
    "testQRTTweet":"https://twitter.com/pdxdylan/status/1611477137319514129",
    "testQrtCeptionTweet":"https://twitter.com/CatherineShu/status/585253766271672320",
    "testQrtVideoTweet":"https://twitter.com/pdxdylan/status/1674561759422578690",
    "testNSFWTweet":"https://twitter.com/kuyacoy/status/1581185279376838657",
    "testPollTweet": "https://twitter.com/norm/status/651169346518056960",
    "testMixedMediaTweet":"https://twitter.com/bigbeerfest/status/1760638922084741177",
}

def getVNFFromLink(link):
    return twitfix.getTweetData(link)

with open('generated.txt', 'w',encoding='utf-8') as f:
    f.write("# autogenerated from testgen.py\n")
    for test in tests:
        f.write(f"{test}=\"{tests[test]}\"\n")
    f.write("\n")
    for test in tests:
        VNF = getVNFFromLink(tests[test])
        del VNF['likes']
        del VNF['retweets']
        del VNF['replies']
        del VNF['user_screen_name']
        del VNF['user_name']
        del VNF['user_profile_image_url']
        del VNF['communityNote']
        # write in a format that can be copy-pasted into a python file, i.e testTextTweet={...
        f.write(f"{test}_compare={VNF}\n")