import { Currency } from '../types';

export const formatCurrency = (amount: number, currency: Currency = 'INR'): string => {
  const absAmount = Math.abs(amount);
  let symbol = '₹';
  let locale = 'en-IN';

  if (currency === 'USD') {
    symbol = '$';
    locale = 'en-US';
  } else if (currency === 'EUR') {
    symbol = '€';
    locale = 'de-DE';
  }

  const formatted = new Intl.NumberFormat(locale, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(absAmount);

  return `${amount < 0 ? '-' : ''}${symbol}${formatted}`;
};

export const formatPercent = (val: number): string => {
  return `${val >= 0 ? '+' : ''}${val.toFixed(1)}%`;
};

