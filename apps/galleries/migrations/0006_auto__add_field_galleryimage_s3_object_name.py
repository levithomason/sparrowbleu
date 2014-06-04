# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GalleryImage.s3_object_name'
        db.add_column(u'galleries_galleryimage', 's3_object_name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 6, 4, 0, 0), max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GalleryImage.s3_object_name'
        db.delete_column(u'galleries_galleryimage', 's3_object_name')


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
            's3_object_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['galleries']