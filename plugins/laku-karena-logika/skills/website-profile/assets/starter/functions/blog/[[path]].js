// /blog, /blog/halaman/N, /blog/kategori/<k>, /blog/<artikel> dari API Lakukan.
import { tangani } from '../_lib/shell.js';
import { blog } from '../_lib/halaman.js';

export const onRequestGet = (ctx) => tangani(ctx, 'blog', blog);
