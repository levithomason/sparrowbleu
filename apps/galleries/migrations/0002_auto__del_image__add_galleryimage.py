# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'galleries_image')

        # Adding model 'GalleryImage'
        db.create_table(u'galleries_galleryimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galleries.Gallery'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'galleries', ['GalleryImage'])


    def backwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'galleries_image', (
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galleries.Gallery'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'galleries', ['Image'])

        # Deleting model 'GalleryImage'
        db.delete_table(u'galleries_galleryimage')


    models = {
        u'galleries.gallery': {
            'Meta': {'object_name': 'Gallery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number_of_images': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'galleries.galleryimage': {
            'Meta': {'object_name': 'GalleryImage'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['galleries.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['galleries']