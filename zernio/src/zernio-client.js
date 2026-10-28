import 'dotenv/config';
import Zernio from '@zernio/node';

if (!process.env.ZERNIO_API_KEY) {
  console.error('ZERNIO_API_KEY manquante. Copiez .env.example vers .env et renseignez votre clé.');
  process.exit(1);
}

export const zernio = new Zernio();
