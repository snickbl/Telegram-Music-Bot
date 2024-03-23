from sqlalchemy import create_engine

engine = create_engine("sqlite:///D:\\PROGRAMMING\\TelegramBot\\cache.db", echo=True)
