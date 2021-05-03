import pyupbit

access = "EL13IF46ku47ex7AxnynmmxHu31Pawiz20CIj7eu"          # 본인 값으로 변경
secret = "zuuaqx3R3PNn6KpJd3UIQSgpivA2kxX1Jurw6xIJ"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 