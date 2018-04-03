import matplotlib.pyplot as plt

from astropy.table import Table

# See https://pipelines.lsst.io/getting-started/multiband-analysis.html

H_cat = Table.read('PTF11mty_H_cat.fits')
J_cat = Table.read('PTF11mty_J_cat.fits')

snr_threshold = 3
good_color = (J_cat['J_SNR'] > snr_threshold) & (H_cat['H_SNR'] > snr_threshold)

H_cat = H_cat[good_color]
J_cat = J_cat[good_color]

plt.scatter(J_cat['J_mag']-H_cat['H_mag'], J_cat['J_mag'])
plt.xlabel('J-H [AB mag]')
plt.ylabel('J [AB mag]')
plt.ylim(23, 12)
plt.show()

plt.scatter(J_cat['J_mag'], H_cat['H_mag'])
plt.xlabel('J [AB mag]')
plt.ylabel('H [AB mag]')
plt.show()

plt.scatter(H_cat['H_mag'], H_cat['H_mag_err'], label='H', color='green')
plt.scatter(J_cat['J_mag'], J_cat['J_mag_err'], label='J', color='blue')
plt.xlabel('AB mag')
plt.ylabel('mag uncertainty')
plt.legend()
plt.show()
