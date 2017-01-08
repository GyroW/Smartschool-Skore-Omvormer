import cStringIO as StringIO
from twisted.web.client import getPage
from twisted.internet import task
from lxml import etree

url = 'http://localhost/punten/index.html'


def main(reactor):
    return get_content()


def get_content():
    d = getPage(url)
    d.addCallback(parse_html)
    d.addCallback(extract_courses)
    return d


def page_content_printer(html):
    print(html)


def parse_html(html):
    parser = etree.HTMLParser(encoding='utf8')
    tree = etree.parse(StringIO.StringIO(html), parser)
    return tree


def extract_courses(tree):
    vals = tree.xpath('//div[@class="courseList"]/*/div[@class]')
    punten = extract_points(tree)
    i = 0
    for x in range(0, len(vals) - 1, 2):
        name = vals[x][0].text
        teacher = vals[x][1].text
        if len(vals[x+1]) == 0:
            counter = 0
        else:
            counter = vals[x + 1][0].text
        print("Vak: %s, gegeven door: %s en met als punten(%s): " % (name, teacher, counter))
        aantal = int(counter)
        if aantal > 0:
            for x in range(0, aantal):
                print("           punt: %s" % punten[i])
                i += 1
    return tree


def extract_points(tree):
    points = tree.xpath('//div[@class="grid_course_evals"]/div/div')
    punten = []
    for point in points:
        value = point.text
        if value is not None:
            punten.append(value.strip())
    return punten


task.react(main)
