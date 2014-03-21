# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'GalleryImage.is_preview_image'
        db.delete_column(u'galleries_galleryimage', 'is_preview_image')

        # Deleting field 'GalleryImage.large_thumb_url'
        db.delete_column(u'galleries_galleryimage', 'large_thumb_url')

        # Deleting field 'GalleryImage.small_thumb_url'
        db.delete_column(u'galleries_galleryimage', 'small_thumb_url')


    def backwards(self, orm):
        # Adding field 'GalleryImage.is_preview_image'
        db.add_column(u'galleries_galleryimage', 'is_preview_image',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'GalleryImage.large_thumb_url'
        db.add_column(u'galleries_galleryimage', 'large_thumb_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'GalleryImage.small_thumb_url'
        db.add_column(u'galleries_galleryimage', 'small_thumb_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)


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
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_portrait': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['galleries']