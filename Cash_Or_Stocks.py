import numpy as np
import math as m
import matplotlib.pyplot as plt

'''
This assumes yearly contribution is done at the end of the year.
Once you hit the witheld limit, the rest of the money is put into the invested portion until you push the withheld to the invested portion again.
There is no interest or anything on the withheld portion.
For the modified strategy the money is broken up right away by removing the witheld portion.
'''

hist = [.1661,.3169,-.031,.3047, .0762,.1008, .0132, .3758,.2296,.3336,.2858,.2104,-.091,-.1189,-.2210,.2868,.1088,.0491,.1579,.0549,-.3700,.2646,.1506,.0211,.1600,.3239,.1369,.0138,.1196,.2183,-.0438]
mu,sigma = np.mean(hist),np.std(hist)



# Function Inputs
yrs = 25 # yrs to inv
total_amount = 60000 # amount starting with
amount_withheld = 500 # amount for modified
add_per_year = 51000 # amount contributed per yr
ret_cutoff = -0.05 # Cutoff to kick in add
smooth_ret = True # Assume returns can't be greater than 18% or less than -30%
#######################


def calculation(yrs, total_amount, amount_withheld, add_per_year, ret_cutoff, smooth_ret):
	count_mod = 0 # variable specifying the number of modified strategy wins
	count_100 = 0 # variable specifying the number of 100% strategy wins
	max_100_win = 0 # variable capturing the maximum 100% win amount
	max_mod_win = 0 # variable capturing the maximum modified win amount
	#min_100_amount = total_amount # minimum amount recorded during simulation for 100% invested
	#min_mod_amount = total_amount # minimum amount recorded during simulation for modified invested
	trials = 1000 # Number of trials to run
	for i in range(0,trials):
		mod_values = []
		hundred_values = []
		add_mon_yr_count = amount_withheld // add_per_year # How many years it will take to bring the amount withheld back to the expected value
		current_add_mon_yr = add_mon_yr_count
		ret_dirty = np.random.normal(mu,sigma,yrs)
		plt_yrs = np.arange(yrs+1)
		ret = []
		# Smoothing data to take out extremely large numbers
		if smooth_ret:
			for val in ret_dirty:
				if val > 0.18: # Stop returns greater than 18%
					ret.append(0.18)
				elif val < -0.3: # Stop losses greater than 30%
					ret.append(-0.3) 
				else:
					ret.append(val)
		else:
			for val in ret_dirty:
				ret.append(val)
		
		
		# 100% Case
		fv = total_amount
		hundred_values.append(fv)
		for y in range(0,yrs):
			fv = np.fv(ret[y],1,-add_per_year,-fv)
			hundred_values.append(fv)

		# Modified Case
		fv_mod = total_amount - amount_withheld
		mod_values.append(fv_mod)
		for y in range(0,yrs):
			if ret[y] < ret_cutoff: # This is a really down year
				if current_add_mon_yr >= add_mon_yr_count:
					current_add_mon_yr = 0
					fv_mod = np.fv(ret[y],1,-add_per_year,-fv_mod) + amount_withheld
				else:
					fv_mod = np.fv(ret[y],1,0,-fv_mod) + add_per_year*current_add_mon_yr
					current_add_mon_yr = 0
			else: #This is not a big enough drop to rebalance portfolio
				if current_add_mon_yr >= add_mon_yr_count:
					fv_mod = np.fv(ret[y],1,-add_per_year,-fv_mod)
				else:
					current_add_mon_yr += 1
					if add_per_year*current_add_mon_yr > amount_withheld:
						fv_mod = np.fv(ret[y],1,0,-fv_mod) + ((add_per_year*current_add_mon_yr) % amount_withheld) 
					else:
						fv_mod = np.fv(ret[y],1,0,-fv_mod)
			# Add back for final yr
			if y == yrs - 1:
				if current_add_mon_yr >= add_mon_yr_count:
					fv_mod = fv_mod + amount_withheld
				else:
					fv_mod = fv_mod + add_per_year*current_add_mon_yr
			mod_values.append(fv_mod)
			
		# Now calculate and store trial values
		if fv_mod > fv:
			count_mod += 1
			win = (100*(fv_mod-fv)/fv_mod)
			if win > max_mod_win:
				max_mod_win = win
		else:
			count_100 += 1
			win = (100*(fv-fv_mod)/fv)
			if win > max_100_win:
				max_100_win = win
		
	print(ret[y], ret[y-1])

	# Output of function
	print("--------------------------------------------")
	print("100% won {} times".format(count_100))
	print("Modified strategy won {} times".format(count_mod))
	print("The max mod win is {0:2.2f}%".format(max_mod_win))
	print("The max 100 win is {0:2.2f}%".format(max_100_win))
	print("Sanity Check values for last run are 100% {:,} and modified {:,}".format(fv,fv_mod))

	#plt.plot(plt_yrs,mod_values, label='modified')
	#plt.plot(plt_yrs,hundred_values, label='100%')
	#plt.legend(loc='upper left')
	#plt.show()

calculation(yrs, total_amount, amount_withheld, add_per_year, ret_cutoff, smooth_ret)


