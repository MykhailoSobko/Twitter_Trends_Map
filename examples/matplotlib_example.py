import matplotlib.pyplot as plt

tweet_volume = [10000, 12000, 4000, 9000, 15000, 3000, 2500, 1000]

plt.plot(tweet_volume, color='blue')
plt.title('Some trend here', fontsize=14)
plt.xlabel('days', fontsize=14)
plt.ylabel('tweet volume', fontsize=14)
plt.grid(True)
plt.show()
