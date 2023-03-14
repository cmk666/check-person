# -*- coding: utf-8 -*-
# @Author:             cmk666
# @Created time:       2023-03-13 09:55:16
# @Last Modified time: 2023-03-14 13:26:40
from flask import Flask, request, jsonify
import copy
app = Flask('Check person')
d, a, b = {}, {}, set()
with open('raw.txt', encoding = 'utf-8') as f:
	for i in f.readlines():
		if i[0] != '#':
			j, l, n, _1, _2, _3, s, _4, _5 = i.split(',')
			def add(x, y, z):
				global d, a, b
				if x not in d:
					a[x] = []
					d[x] = {}
				if y not in d[x]:
					a[x].append(y)
					d[x][y] = set()
				d[x][y].add(z)
			add(j, l, n)
			add('省份', s, n)
			b.add(n)
a = sorted(a.items())
s = ', '.join('"' + i[0] + '": ["' + '", "'.join(i[1]) + '"]' for i in a)
with open('index.html', encoding = 'utf-8') as f:
	html = f.read().replace('DATA', s)
@app.get('/')
def index():
	return html
@app.get('/get')
def getdata():
	try:
		res = copy.copy(b)
		val = request.args.get('t', None)
		if val:
			for i in map(int, val.split(',')):
				x, y = i // 100, i % 100
				res &= d[a[x][0]][a[x][1][y]]
		data = { 'status': 'ok', 'count': len(res) }
		if len(res) <= 100:
			data['result'] = list(res)
	except:
		data = { 'status': 'fail' }
	return jsonify(data)
app.run('127.0.0.1', 8888)