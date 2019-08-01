from app.models.models import *

'''
表的初始化
'''


def major_init():
    session = Session()

    session.add_all(
        [
            Major(title='Python基础', duration=20, order=1),
            Major(title='Web前端', duration=6, order=2),
            Major(title='MySQL', duration=4, order=3),
            Major(title='Web后端', duration=20, order=4),
            Major(title='中期项目', duration=10, order=5),
            Major(title='爬虫', duration=15, order=6),
            Major(title='后期项目', duration=15, order=7),
            Major(title='AI训练营', duration=20, order=8),
        ]
    )
    session.commit()
    session.close()


def teacher_init():
    session = Session()

    session.add_all(
        [
            Teacher(name='韩博文'),
            Teacher(name='侯秋娜'),
            Teacher(name='矫键'),
            Teacher(name='李小波'),
            Teacher(name='毛信宇'),
            Teacher(name='徐鑫'),
            Teacher(name='张意林'),
            Teacher(name='赵鹏飞')
        ]
    )
    session.commit()
    session.close()


def association_init():
    def association_append(**kwargs):
        teacher_obj = session.query(Teacher).filter_by(name=kwargs.get('name')).first()
        major_obj = session.query(Major).filter_by(title=kwargs.get('title')).first()
        teacher_obj.major.append(major_obj)

    session = Session()

    association_append(name='李小波', title='Python基础')
    association_append(name='李小波', title='Web前端')
    association_append(name='李小波', title='MySQL')
    association_append(name='李小波', title='Web后端')
    association_append(name='赵鹏飞', title='Python基础')
    association_append(name='赵鹏飞', title='爬虫')
    association_append(name='侯秋娜', title='Python基础')
    association_append(name='侯秋娜', title='Web前端')
    association_append(name='侯秋娜', title='MySQL')
    association_append(name='侯秋娜', title='Web后端')
    association_append(name='毛信宇', title='中期项目')
    association_append(name='毛信宇', title='后期项目')
    association_append(name='毛信宇', title='MySQL')
    association_append(name='毛信宇', title='Web后端')
    association_append(name='韩博文', title='爬虫')
    association_append(name='韩博文', title='AI训练营')
    association_append(name='徐鑫', title='中期项目')
    association_append(name='徐鑫', title='后期项目')
    association_append(name='徐鑫', title='爬虫')
    association_append(name='矫键', title='中期项目')
    association_append(name='矫键', title='Python基础')
    association_append(name='矫键', title='Web前端')
    association_append(name='张意林', title='AI训练营')

    session.commit()
    session.close()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    major_init()
    teacher_init()
    association_init()
