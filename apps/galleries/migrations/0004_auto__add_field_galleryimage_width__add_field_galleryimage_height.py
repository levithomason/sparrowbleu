# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GalleryImage.width'
        db.add_column(u'galleries_galleryimage', 'width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'GalleryImage.height'
        db.add_column(u'galleries_galleryimage', 'height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GalleryImage.width'
        db.delete_column(u'galleries_galleryimage', 'width')

        # Deleting field 'GalleryImage.height'
        db.delete_column(u'galleries_galleryimage', 'height')


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
            'is_preview_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'small_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['galleries']