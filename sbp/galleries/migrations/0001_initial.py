# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gallery'
        db.create_table(u'galleries_gallery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('passcode', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'galleries', ['Gallery'])

        # Adding model 'Image'
        db.create_table(u'galleries_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galleries.Gallery'])),
        ))
        db.send_create_signal(u'galleries', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table(u'galleries_gallery')

        # Deleting model 'Image'
        db.delete_table(u'galleries_image')


    models = {
        u'galleries.gallery': {
            'Meta': {'object_name': 'Gallery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'galleries.image': {
            'Meta': {'object_name': 'Image'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['galleries.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['galleries']