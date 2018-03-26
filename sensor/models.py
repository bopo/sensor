MACHINE = {
    '01': {
        'title': '01 scheda NET*',
        'start': [b'#01STS 1 EF.', ['*01']],
        'close': [b'#01STS 0 EE.', ['*01']],
        'clock': [b'#01SIT 10 15.', ['*018B.']],
        'stats': [b'#01?RWI 179 96.', [
                '*010001B.',    # 开
                '*010031E.',    # 关
                '*010041F.',    # 冷
            ],
        ],
    },

    '02': {
        'title': '02 scheda MCE',
        'start': [b'#02STS 1 F0.', ['*028C.']],
        'close': [b'#02STS 0 EF.', ['*028C.']],
        'clock': [b'#02SIT 10 16.', ['*028C.']],
        'stats': [b'#02?RWI 179 97.', [
                '*028C4.',      # 开
                '*023BF.',      # 关
                '*024C4.',      # 冷
            ],
        ],
    },

    '03': {
        'title': '03 scheda Softec',
        'start': [b'#03STS 1 F1.', ['*038D.']],
        'close': [b'#03STS 0 F0.', ['*038D.']],
        'clock': [b'#03SIT 10 17.', ['*038D.']],
        'clock': [b'#03?SWVC5.', ['*03EUROSUN V1.4C7.']],
        'stats': [b'#03?RWI 179 98.', [
                '*0308429.',    # 开
                '*0307125.',    # 关
                '*0306427.'     # 冷
            ],
        ],
    },

    '05': {
        'title': '05 scheda PotPlus',
        'start': [b'#05STS 1 F3.', ['*05STS 1 FA.']],
        'close': [b'#05STS 0 F2.', ['*05STS 0 F9.']],
        'clock': [b'##05SIT 10 19.', ['*05SIT 10 20.']],
        'clock': [b'#01?SWVC3.', ['*01SOCOSUN NET_SUN V1.71D.']],
        'stats': [b'#05?RWI 179 9A.', [
                '*0500827.',    # 开
                '*0500322.',    # 关
                '*0500423.',    # 冷
            ],
        ],
    },            
}