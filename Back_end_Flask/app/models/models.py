import os

from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

db_file_name = 'course_system.db'  # SQLite文件名
path = os.path.abspath(__file__)  # 当前文件路径
db_file_path = os.path.join(os.path.dirname(path), db_file_name)  # SQLite文件所在路径
# sqlite默认建立的对象只能让建立该对象的线程使用，而sqlalchemy是多线程的
# 所以我们需要指定check_same_thread=False来让建立的对象任意线程都可使用
engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_file_path), echo=False)  # 创建数据库连接
Base = declarative_base()  # 建立基本映射类，用于继承
Session = sessionmaker(bind=engine)  # 创建CRUD的会话类
# session = Session()  # Session类实例化

# 教师与课程 多对多关联表
association_table = Table(
    'association', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('teacher_id', Integer, ForeignKey('teacher.id', ondelete='CASCADE')),
    Column('major_id', Integer, ForeignKey('major.id', ondelete='CASCADE'))
)


# 教师
class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String())

    def __repr__(self):
        return self.name


# 课程
class Major(Base):
    __tablename__ = 'major'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String())
    duration = Column(Integer())
    order = Column(Integer(), unique=True)
    is_show = Column(Boolean(), default=True)

    teacher = relationship(
        'Teacher', secondary=association_table, lazy='dynamic',
        backref=backref('major', lazy='dynamic'),
        cascade='delete, delete-orphan', single_parent=True,
    )

    def __repr__(self):
        return self.title

    @property
    def info(self):
        return {
            'id': self.id,
            'title': self.title,
            'options': [teacher.name for teacher in self.teacher],
            'duration': self.duration
        }


# 班级
class ClassName(Base):
    __tablename__ = 'class_name'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    class_name = Column(String())
    is_show = Column(Boolean(), default=True)

    @property
    def info(self):
        return {
            'id': self.id,
            'className': self.class_name,
        }


# 存档
class Archive(Base):
    __tablename__ = 'archive'

    class_id = Column(Integer(), primary_key=True)
    major_id = Column(Integer(), primary_key=True)
    info = Column(String())


# 用户
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(), unique=True)
    password = Column(String())


if __name__ == '__main__':
    # 建表
    Base.metadata.create_all(engine)
