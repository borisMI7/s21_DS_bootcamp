import financial as fn


def test_find():
    txt = fn.getHTML('TSLA')
    soup = fn.BeautifulSoup(txt, 'lxml')
    table = soup.find('div', class_ = 'tableBody yf-9ft13')

    assert fn.find("Total Revenue", table)[0] == 'Total Revenue'
    assert fn.find("Total Revenue", table)[1] == '97,690,000.00'
    assert fn.find("Total Revenue", table)[2] == '97,690,000.00'
    assert type(fn.find("Total Revenue", table)) == type((1, 2, 3))

def test_findExp():
    exp = None
    txt = fn.getHTML('TSLA')
    soup = fn.BeautifulSoup(txt, 'lxml')
    table = soup.find('div', class_ = 'tableBody yf-9ft13')
    try:
        fn.find("TSLA", table)
    except Exception as e:
        exp = e
    assert exp != None

