# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u82f1\u96c4\u540d\u79f0')),
                ('warrior_id', models.IntegerField(verbose_name='\u521d\u59cb\u5316\u82f1\u96c4')),
                ('career', models.IntegerField(verbose_name='\u804c\u4e1a')),
                ('equipFates_int', models.CharField(default=b'', max_length=200, verbose_name='\u88c5\u5907\u7f18\u5206')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardId', models.IntegerField(default=0, verbose_name='\u82f1\u96c4ID ')),
                ('name', models.CharField(max_length=200, verbose_name='\u82f1\u96c4\u540d\u79f0')),
                ('upgrade', models.IntegerField(verbose_name='\u8fdb\u9636\u52a0\u51e0')),
                ('evolveHero_id', models.IntegerField(default=0, verbose_name='\u8fdb\u9636\u76ee\u6807\u82f1\u96c4')),
                ('evolveLevel', models.IntegerField(default=0, verbose_name='evolveLevel')),
                ('evolveSoulCost', models.IntegerField(default=0, verbose_name='evolveSoulCount')),
                ('evolveCosts_int', models.CharField(default=b'', max_length=100, verbose_name='evolveCosts')),
                ('soulId', models.IntegerField(default=0, verbose_name='soulId')),
                ('maxLevel', models.IntegerField(verbose_name='maxLevel')),
                ('attack', models.FloatField(verbose_name='\u57fa\u7840\u653b\u5f3a')),
                ('trainAttackMax', models.FloatField(default=0, verbose_name='\u57f9\u517b\u653b\u5f3a\u4e0a\u9650')),
                ('hp', models.FloatField(verbose_name='\u57fa\u7840\u8840\u91cf')),
                ('trainHpMax', models.FloatField(default=0, verbose_name='\u57f9\u517b\u8840\u91cf\u4e0a\u9650')),
                ('physicalArmor', models.FloatField(verbose_name='\u57fa\u7840\u7269\u9632')),
                ('trainPhysicalArmorMax', models.FloatField(default=0, verbose_name='\u57f9\u517b\u7269\u9632\u4e0a\u9650')),
                ('magicArmor', models.FloatField(verbose_name='\u57fa\u7840\u6cd5\u9632')),
                ('trainMagicArmorMax', models.FloatField(default=0, verbose_name='\u57f9\u517b\u6cd5\u9632\u4e0a\u9650')),
                ('realPhysical', models.FloatField(default=0, verbose_name='\u7a7f\u7532')),
                ('realMagic', models.FloatField(default=0, verbose_name='\u6cd5\u7a7f')),
                ('shoot', models.FloatField(verbose_name='\u57fa\u7840\u547d\u4e2d')),
                ('dodge', models.FloatField(verbose_name='\u57fa\u7840\u95ea\u907f')),
                ('critical', models.FloatField(verbose_name='\u57fa\u7840\u66b4\u51fb')),
                ('tenacity', models.FloatField(verbose_name='\u57fa\u7840\u97e7\u6027')),
                ('damageFree', models.FloatField(verbose_name='\u989d\u5916\u51cf\u4f24')),
                ('powerRank', models.FloatField(default=0, verbose_name='\u57fa\u7840\u6218\u6597\u529b')),
                ('energyPerSec', models.FloatField(verbose_name='\u6bcf\u79d2\u56de\u80fd')),
                ('maxEnergy', models.IntegerField(verbose_name='\u6700\u5927\u80fd\u91cf')),
                ('quality', models.IntegerField(default=0, verbose_name='\u54c1\u8d28')),
                ('category', models.IntegerField(default=0, verbose_name='\u5206\u7c7b')),
                ('violence', models.FloatField(verbose_name='\u66b4\u51fb\u500d\u7387')),
                ('killToHeal', models.FloatField(verbose_name='\u51fb\u6740\u56de\u8840')),
                ('killToEnergy', models.FloatField(verbose_name='\u51fb\u6740\u56de\u80fd')),
                ('hpPerSecond', models.FloatField(verbose_name='\u6bcf\u79d2\u56de\u8840')),
                ('heroTeamId', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u7ec4id')),
                ('collectionRecoverEnergy', models.FloatField(default=0, verbose_name='\u6536\u96c6\u56de\u80fd')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrType', models.CharField(max_length=200, verbose_name='attrType')),
                ('extra', models.FloatField(default=0, verbose_name='extra')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroBubble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heroId', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u7684Id')),
                ('bornTypeMessage_str', models.CharField(max_length=500)),
                ('initPointTypeMessage_str', models.CharField(max_length=500)),
                ('gatherPointTypeMessage_str', models.CharField(max_length=500)),
                ('initAttackTypeMessage_str', models.CharField(max_length=500)),
                ('strokesTypeMessage_str', models.CharField(max_length=500)),
                ('hpLowTypeMessage_str', models.CharField(max_length=500)),
                ('friendsHpLowTypeMessage_str', models.CharField(max_length=500)),
                ('deadTypeMessage_str', models.CharField(max_length=500)),
                ('friendsDeadTypeMessage_str', models.CharField(max_length=500)),
                ('normalAttackTypeMessage_str', models.CharField(max_length=500)),
                ('bornTypeProperbility', models.FloatField(default=0.0)),
                ('initPointTypeProperbility', models.FloatField(default=0.0)),
                ('gatherPointTypeProperbility', models.FloatField(default=0.0)),
                ('initAttackTypeProperbility', models.FloatField(default=0.0)),
                ('strokesTypeProperbility', models.FloatField(default=0.0)),
                ('hpLowTypeProperbility', models.FloatField(default=0.0)),
                ('friendsHpLowTypeProperbility', models.FloatField(default=0.0)),
                ('deadTypeProperbility', models.FloatField(default=0.0)),
                ('friendsDeadTypeProperbility', models.FloatField(default=0.0)),
                ('normalAttackTypeProperbility', models.FloatField(default=0.0)),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroCombat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atk', models.FloatField(default=0.0)),
                ('hp', models.FloatField(default=0.0)),
                ('armor', models.FloatField(default=0.0)),
                ('magArmor', models.FloatField(default=0.0)),
                ('phyPenetr', models.FloatField(default=0.0)),
                ('magPenetr', models.FloatField(default=0.0)),
                ('hitin', models.FloatField(default=0.0)),
                ('dodge', models.FloatField(default=0.0)),
                ('crit', models.FloatField(default=0.0)),
                ('toughness', models.FloatField(default=0.0)),
                ('etrAtkReduc', models.FloatField(default=0.0)),
                ('energy', models.FloatField(default=0.0)),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroDestiny',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=1, verbose_name='\u5929\u547d\u7b49\u7ea7')),
                ('stoneCost', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u5929\u547d\u77f3')),
                ('heroLevel', models.IntegerField(default=0, verbose_name='\u9700\u8981\u73a9\u5bb6\u7684\u7b49\u7ea7')),
                ('extra', models.FloatField(default=0, verbose_name='\u5c5e\u6027\u6210\u957f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroEquipFatesAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipId', models.IntegerField(default=0, verbose_name='\u88c5\u5907id')),
                ('attrType', models.CharField(max_length=200, verbose_name='\u5c5e\u6027\u7c7b\u522b')),
                ('extra', models.FloatField(default=0, verbose_name='\u5c5e\u6027\u63d0\u5347')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroEvolveCosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xp', models.IntegerField(verbose_name='xp')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField(default=0, verbose_name='\u7c7b\u522b')),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('attrList_int', models.CharField(default=b'', max_length=100, verbose_name='\u5c5e\u6027\u914d\u7f6e')),
                ('descriptionId', models.CharField(default=b'', max_length=100, verbose_name='\u63cf\u8ff0\u4fe1\u606f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maxStar', models.IntegerField(verbose_name='maxStar')),
                ('skill0', models.IntegerField(verbose_name='skill0')),
                ('skill0Lv', models.IntegerField(verbose_name='skill0Lv')),
                ('skillinfo_int', models.CharField(default=b'', max_length=200, verbose_name='skillinfo_int')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroStar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardId', models.IntegerField(default=0, verbose_name='\u82f1\u96c4ID')),
                ('star', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u661f\u7ea7')),
                ('attackGrow', models.FloatField(default=0, verbose_name='\u653b\u51fb\u529b\u6210\u957f')),
                ('hpGrow', models.FloatField(default=0, verbose_name='\u8840\u91cf\u6210\u957f')),
                ('physicalArmorGrow', models.FloatField(default=0, verbose_name='\u62a4\u7532\u6210\u957f')),
                ('magicArmorGrow', models.FloatField(default=0, verbose_name='\u9b54\u6297\u6210\u957f')),
                ('realPhysicalGrow', models.FloatField(default=0, verbose_name='\u7269\u7a7f\u6210\u957f')),
                ('realMagicGrow', models.FloatField(default=0, verbose_name='\u6cd5\u7a7f\u6210\u957f')),
                ('shootGrow', models.FloatField(default=0, verbose_name='\u547d\u4e2d\u6210\u957f')),
                ('dodgeGrow', models.FloatField(default=0, verbose_name='\u95ea\u907f\u6210\u957f')),
                ('criticalGrow', models.FloatField(default=0, verbose_name='\u66b4\u51fb\u6210\u957f')),
                ('tenacityGrow', models.FloatField(default=0, verbose_name='\u97e7\u6027\u6210\u957f')),
                ('damageFreeGrow', models.FloatField(default=0, verbose_name='\u989d\u5916\u51cf\u4f24\u6210\u957f')),
                ('energyPerSecGrow', models.FloatField(default=0, verbose_name='\u6bcf\u79d2\u56de\u80fd\u6210\u957f')),
                ('growPercent', models.FloatField(default=0, verbose_name='\u6210\u957f\u767e\u5206\u6bd4')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroStarUpgrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('soulCount', models.IntegerField(verbose_name='\u6d88\u8017soul\u6570\u91cf')),
                ('costs_int', models.CharField(default=b'', max_length=100, verbose_name='costs')),
                ('sepecialItemMaxCount', models.IntegerField(verbose_name='\u6d88\u8017\u7279\u6b8a\u7269\u54c1\u6570\u91cf\u4e0a\u9650')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroStarUpgradeCosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heroCardIds_int', models.CharField(default=b'', max_length=100, verbose_name='\u76f8\u5e94\u7ec4\u91cc\u9762\u6240\u6709\u82f1\u96c4cardid')),
                ('descriptionId', models.CharField(default=0, max_length=200, verbose_name='descId')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='nameId')),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroTeamAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrType', models.CharField(max_length=200, verbose_name='attrType')),
                ('extra', models.FloatField(default=0, verbose_name='extra')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroTeamLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamId', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u7ec4\u7684Id')),
                ('level', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u7ec4\u7684\u7ea7\u522b')),
                ('score', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u7ec4\u7684\u79ef\u5206')),
                ('costs_int', models.CharField(default=0, max_length=100, verbose_name='\u82f1\u96c4\u7ec4\u5347\u7ea7\u7684\u6d88\u8017')),
                ('attrList_int', models.CharField(default=b'', max_length=100, verbose_name='\u5c5e\u6027\u914d\u7f6e')),
                ('nextLevelId', models.IntegerField(default=0, verbose_name='\u4e0b\u4e00\u4e2a\u7ea7\u522b\u7684\u4e3b\u952e')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroTeamLevelCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='HeroTrain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u57f9\u517b\u4e39\u7684\u6570\u91cf')),
                ('goldCost', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u91d1\u5e01\u7684\u6570\u91cf')),
                ('diamondCost', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u94bb\u77f3\u7684\u6570\u91cf')),
                ('hpAttrValues_int', models.CharField(default=b'', max_length=500, verbose_name='\u8840\u91cf\u5c5e\u6027\u7684\u589e\u52a0\u51cf\u5c11\u503c')),
                ('magicAttrValues_int', models.CharField(default=b'', max_length=500, verbose_name='\u9b54\u6cd5\u9632\u5fa1\u5c5e\u6027\u7684\u589e\u52a0\u51cf\u5c11\u503c')),
                ('physicalAttrValues_int', models.CharField(default=b'', max_length=500, verbose_name='\u7269\u7406\u9632\u5fa1\u5c5e\u6027\u7684\u589e\u52a0\u51cf\u5c11\u503c')),
                ('attackAttrValues_int', models.CharField(default=b'', max_length=500, verbose_name='\u653b\u51fb\u5c5e\u6027\u7684\u589e\u52a0\u51cf\u5c11\u503c')),
                ('itemProbabilities_int', models.CharField(default=b'', max_length=100, verbose_name='\u57f9\u517b\u4e39\u5bf9\u5e94\u5c5e\u6027\u7684\u6743\u91cd')),
                ('goldProbabilities_int', models.CharField(default=b'', max_length=100, verbose_name='\u91d1\u5e01\u5bf9\u5e94\u5c5e\u6027\u7684\u6743\u91cd')),
                ('diamondProbabilities_int', models.CharField(default=b'', max_length=100, verbose_name='\u94bb\u77f3\u5bf9\u5e94\u5c5e\u6027\u7684\u6743\u91cd')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Warrior',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u82f1\u96c4\u540d\u79f0')),
                ('cardId', models.IntegerField(verbose_name='cardId as gid')),
                ('attackedPoint', models.CharField(default=b'', max_length=200, verbose_name='attackedPoint')),
                ('attackRange', models.IntegerField(default=0, verbose_name='attackRange')),
                ('attackSpan', models.IntegerField(default=0, verbose_name='attackSpan')),
                ('category', models.IntegerField(verbose_name='\u5361\u7684\u7c7b\u578b\uff08\u5c0f\u5175\u8fd8\u662f\u82f1\u96c4\uff09')),
                ('chestPositionX', models.FloatField(default=0, verbose_name='\u80f8\u90e8\u4f4d\u7f6e\u504f\u79fb\u91cf')),
                ('chestPositionY', models.FloatField(default=0, verbose_name='\u80f8\u90e8\u4f4d\u7f6e\u504f\u79fb\u91cf')),
                ('chestPositionZ', models.FloatField(default=0, verbose_name='\u80f8\u90e8\u4f4d\u7f6e\u504f\u79fb\u91cf')),
                ('deadBonePoint_char', models.CharField(max_length=200, verbose_name='\u6b7b\u4ea1\u7279\u6548\u4f4d\u7f6e')),
                ('deadEffect_char', models.CharField(default=b'', max_length=200, verbose_name='\u6b7b\u4ea1\u7279\u6548')),
                ('deadEffectDelay_float', models.CharField(default=0, max_length=200, verbose_name='\u6b7b\u4ea1\u7279\u6548\u5ef6\u8fdf')),
                ('descriptionId', models.CharField(default=0, max_length=200, verbose_name='descId')),
                ('height', models.IntegerField(verbose_name='\u9ad8\u5ea6')),
                ('hurtRate', models.FloatField(verbose_name='\u53d7\u51fb\u65f6\u95f4\u500d\u7387')),
                ('downRate', models.FloatField(default=1, verbose_name='\u88ab\u51fb\u5012\u65f6\u95f4\u500d\u7387')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='\u56fe\u6807')),
                ('modelName', models.CharField(max_length=200, verbose_name='\u6a21\u578b\u540d\u79f0')),
                ('moveActRate', models.FloatField(default=0, verbose_name='moveActRate')),
                ('moveSpeed', models.FloatField(verbose_name='\u79fb\u52a8\u901f\u5ea6')),
                ('nameId', models.CharField(max_length=200, verbose_name='nameId')),
                ('population', models.IntegerField(default=0, verbose_name='population')),
                ('width', models.IntegerField(verbose_name='\u5bbd\u5ea6')),
                ('nextWarriorID', models.IntegerField(default=0, verbose_name='\u5c0f\u5175\u4e0b\u4e00\u4e2a\u5f62\u6001\u5c0f\u5175ID')),
                ('nextWarriorLevel', models.IntegerField(default=0, verbose_name='\u5c0f\u5175\u4e0b\u4e2a\u5f62\u6001\u5c0f\u5175\u7b49\u7ea7')),
                ('searchRange', models.FloatField(default=0, verbose_name='\u5bfb\u602a')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='WarriorLevel',
            fields=[
                ('id', models.BigIntegerField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('warrior_id', models.IntegerField(verbose_name='\u5c0f\u5175ID')),
                ('ap', models.FloatField(verbose_name='\u6cd5\u5f3a')),
                ('attack', models.FloatField(verbose_name='\u653b\u5f3a')),
                ('hp', models.FloatField(verbose_name='\u751f\u547d')),
                ('magicArmor', models.FloatField(verbose_name='\u9b54\u6297')),
                ('physicalArmor', models.FloatField(verbose_name='\u62a4\u7532')),
                ('powerRank', models.IntegerField(default=0, verbose_name='powerRank')),
                ('level', models.IntegerField(verbose_name='\u7b49\u7ea7')),
                ('shoot', models.FloatField(verbose_name='\u547d\u4e2d')),
                ('skills_int', models.CharField(default=b'', max_length=200, verbose_name='skills')),
                ('skill0', models.IntegerField(default=0, verbose_name='skill0')),
                ('skill0Lv', models.IntegerField(default=0, verbose_name='skill0Lv')),
                ('dodge', models.FloatField(verbose_name='\u95ea\u907f')),
                ('tenacity', models.FloatField(verbose_name='\u97e7\u6027')),
                ('critical', models.FloatField(verbose_name='\u66b4\u51fb')),
                ('violence', models.FloatField(verbose_name='\u66b4\u51fb\u500d\u7387')),
                ('hpPerSecond', models.FloatField(verbose_name='\u6bcf\u79d2\u56de\u8840')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
