import os

from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db_file_name = 'course_system.db'  # SQLite文件名
path = os.path.abspath(__file__)  # 当前文件路径
db_file_path = os.path.join(path, '..', db_file_name)  # SQLite文件所在路径
# sqlite默认建立的对象只能让建立该对象的线程使用，而sqlalchemy是多线程的
# 所以我们需要指定check_same_thread=False来让建立的对象任意线程都可使用
engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_file_path), echo=False)  # 创建数据库连接
Base = declarative_base()  # 建立基本映射类，用于继承
Session = sessionmaker(bind=engine)  # 创建CRUD的会话类
# session = Session()  # Session类实例化

association_table = Table('association', Base.metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('teacher_id', Integer, ForeignKey('teacher.id')),
                          Column('major_id', Integer, ForeignKey('major.id'))
                          )


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String())
    major = relationship('Major', secondary=association_table, backref='teacher')

    def __repr__(self):
        return self.name


class Major(Base):
    __tablename__ = 'major'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String())
    duration = Column(Integer())

    def __repr__(self):
        return self.title


class Archive(Base):
    __tablename__ = 'archive'

    time = Column(Float(), primary_key=True)
    info = Column(String())


if __name__ == '__main__':
    # 建表
    Base.metadata.create_all(engine)
