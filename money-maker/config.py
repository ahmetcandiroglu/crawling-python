dollar = {
    'intervals': [5, 15, 60, 24*60],

    'investing': {
        'url': 'https://www.investing.com/currencies/usd-try',
        'css': 'table.technicalSummaryTbl tr:nth-of-type(4) td',
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/67.0.3396.99 Safari/537.36'},
    },

    'banks': {
        'enpara': {
            'url': 'https://www.qnbfinansbank.enpara.com/doviz-kur-bilgileri/doviz-altin-kurlari.aspx',
            'sell_css': '#pnlContent dl:nth-of-type(1) span:nth-of-type(2)',
            'buy_css': '#pnlContent dl:nth-of-type(1) span:nth-of-type(3)',
            'name': 'enpara.com'
        }
    },
}

