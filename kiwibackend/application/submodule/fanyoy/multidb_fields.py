# -*- coding:utf-8 -*-
""" 封装多数据库支持的manager"""
from django.conf import settings
from django.core import exceptions
from django.db import models
from django.db import router
from django.db.models.query import QuerySet

class MultiDBSouthField(models.IntegerField):
    """ 这个类不再程序中使用，主要是用来欺骗south不让它在
    数据库中建立外键关系而只建立IntegerField对应的整型字段
    """

    #south时忽略参数
    IGNORE_ARGS = ['related_name', 'on_delete']
    
    def __init__(self, *args, **kargs):         
        for ignore_arg in MultiDBSouthField.IGNORE_ARGS:
            if ignore_arg in kargs:
                del kargs[ignore_arg]

        return super(MultiDBSouthField,self).__init__(*args, **kargs)

    def get_attname(self):
        return '%s_id' % self.name

    def get_attname_column(self):
        attname = self.get_attname()
        column = attname
        return attname, column

class ForeignKeyAcrossDb(models.ForeignKey):
    """ 模拟外键关系"""
    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        models.Field.validate(self, value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.rel.to, instance=model_instance)
        qs = self.rel.to._default_manager.using(using).filter(
                **{self.rel.field_name: value}
             )

        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise exceptions.ValidationError(self.error_messages['invalid'] % {
                'model': self.rel.to._meta.verbose_name, 'pk': value})

    def south_field_triple(self):
        try:
            from south.modelsinspector import introspector
            cls_name = '%s.%s' % (self.__class__.__module__ , 'MultiDBSouthField')
            args, kwargs = introspector(self)

            #因为mysql不支持跨库的外键关系，不在数据库中构建外键关系
            if 'to' in kwargs:
                del kwargs['to']
        
            #数据库建立索引 
            if 'db_index' not in kwargs:
                kwargs['db_index'] = True

            return cls_name, args, kwargs
        except ImportError:
            pass

class OneToOneAcrossDb(models.OneToOneField):
    """ 模拟一对一关系"""
    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        models.Field.validate(self, value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.rel.to, instance=model_instance)
        qs = self.rel.to._default_manager.using(using).filter(
                **{self.rel.field_name: value}
             )

        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise exceptions.ValidationError(self.error_messages['invalid'] % {
                'model': self.rel.to._meta.verbose_name, 'pk': value})

    def south_field_triple(self):
        try:
            from south.modelsinspector import introspector
            cls_name = '%s.%s' % (self.__class__.__module__ , 'MultiDBSouthField')
            args, kwargs = introspector(self)

            #因为mysql不支持跨库的外键关系，不在数据库中构建外键关系
            if 'to' in kwargs:
                del kwargs['to']

            #数据库建立索引 
            if 'db_index' not in kwargs:
                kwargs['db_index'] = True

            return cls_name, args, kwargs
        except ImportError:
            pass
