#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:21:49 2023

@author: shbshka
"""
from django.urls import path
import pages.views as p_views

urlpatterns = [
    path('users', p_views.get_users),
    ]
