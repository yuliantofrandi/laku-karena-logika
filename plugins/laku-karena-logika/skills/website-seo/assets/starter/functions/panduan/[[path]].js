// /panduan, /panduan/<kategori>, /panduan/<kategori>/<artikel> dari API Lakukan.
import { tangani } from '../_lib/shell.js';
import { panduan } from '../_lib/halaman.js';

export const onRequestGet = (ctx) => tangani(ctx, 'panduan', panduan);
