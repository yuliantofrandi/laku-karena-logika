// /portfolio, /portfolio/ai, /portfolio/<artikel> dari API Lakukan (preset jasa; aktif bila menu Portfolio ada).
import { tangani } from '../_lib/shell.js';
import { portfolio } from '../_lib/halaman.js';

export const onRequestGet = (ctx) => tangani(ctx, 'portfolio', portfolio);
