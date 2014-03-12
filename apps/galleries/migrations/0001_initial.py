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
            ('number_of_images', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cost_per_extra_image', self.gf('django.db.models.fields.PositiveIntegerField')(default=20.0)),
        ))
        db.send_create_signal(u'galleries', ['Gallery'])

        # Adding model 'GalleryImage'
        db.create_table(u'galleries_galleryimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galleries.Gallery'])),
            ('is_preview_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_selected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('full_size_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('large_thumb_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('small_thumb_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'galleries', ['GalleryImage'])


    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table(u'galleries_gallery')

        # Deleting model 'GalleryImage'
        db.delete_table(u'galleries_galleryimage')


    models = {
        u'galleries.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'cost_per_extra_image': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number_of_images': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'galleries.galleryimage': {
            'Meta': {'object_name': 'GalleryImage'},
            'full_size_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['galleries.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_preview_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'small_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['galleries']