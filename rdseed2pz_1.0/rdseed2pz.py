#Packages
import numpy as np
import os
import datetime

#FUNCTIONS
###
###
###
#Function that extract the line range to find the parameters according to event dates and intrumentation dates
#Argument is the lines of the file in array format
#Return two values which be the ranges of where to look in the rdseed response file.
def finding_ranges(lines):
	ranges = [0,999999]
	for i in range(len(lines)):
		if 'B052F22' in lines[i]:
        
			y_seed = int(lines[i][25:29])
            #JULIAN DAY
			d_seed = int(lines[i][30:33])
			h_seed = int(lines[i][34:36])
			m_seed = int(lines[i][37:39])
			s_seed = int(lines[i][40:42])
			ms_seed = int(lines[i][43:])
        
            #Compare dates between changes in instrumentation and events. Julian day is converted to Gregorian calendar
			start_date = datetime.datetime(y_seed, 1, 1, h_seed, m_seed, s_seed, ms_seed) + datetime.timedelta(d_seed)
			event_date = datetime.datetime(raw_yy, raw_mt, raw_dd, raw_hh, raw_mm, raw_ss, raw_ms)
        
			if(event_date >= start_date):
				ranges[0] = i
			else:
				ranges[1] = i
				break
        #dates.append([int[l[i][25:29]),int(),int(),int(),int(),float()])
	if(ranges[1] == 999999):
		ranges[1] = len(lines)
	if(ranges[0] == 0):
		#Event was before the first installation of the station or calibration.\nResponse file of this station will not be generated for this event.'
		return(['NO','NO'])
	else:
		return(ranges[0],ranges[1])

#Function for the extraction of data
#Function takes as arguments the minimum and maximos range of lines to find based date instrumentation for the event.
#Also take the lines of the file as an array.
#Return Normalization factor, inverse of channel sensitivity, numbers of zeros & poles, and array of zeros and poles.
#(all in string format) ready for writing.
def extraction_data(s_min, s_max, lines):
    
    #define variable to save poles and zeros
	zeros=[]
	poles=[]
    
	for i in range(s_min, s_max):
        #Extraction of normalization factor A0
		if 'B053F05' in lines[i]:
			unit = lines[i][51:54]
		if 'B053F07' in lines[i]:
			A0 = float(lines[i][51:])
        
        #Extraction of channel sensitivity and inverse sensitivity
        #B058F04 line is in two lines, so another parameter must be fulfilled
	#Evaluate if Sensitivity if not in Meters/Sec. In casi is in Radians, a convertion must be done.
		if(('B058F04' in lines[i]) and ('Sensitivity' in lines[i])):
			if unit == 'M/S':
				sens =  float(lines[i][51:])
			#else:
				#factor = 
				#sens = float(lines[i][51:])*factor
			inv_sens = 1/sens

        #Extraction of complex parts
        #Extraction of the numbers of zeros and poles
		if 'B053F09' in lines[i]:
			n_zeros = int(lines[i][51:])
            
		if 'B053F14' in lines[i]:
			n_poles = int(lines[i][51:])
        
        #Extraction of complex zeros
		if 'B053F10-13' in lines[i]:
			zeros.append([ '{:.6E}'.format(float(lines[i][15:29])), '{:.6E}'.format(float(lines[i][29:43])) ])
        
        #Extraction of complex poles
		if 'B053F15-18' in lines[i]:
			poles.append([ '{:.6E}'.format(float(lines[i][15:29])), '{:.6E}'.format(float(lines[i][29:43])) ])
            
	if raw_ext == '1':
		del zeros[-1]
		n_zeros = n_zeros-1
            
	return(str(A0), str(inv_sens), str(n_zeros), str(n_poles), np.asarray(zeros), np.asarray(poles))

###
###
###

#Input data
print('------------------------------------------------------------\n')
print('--- IRIS (rdseed) to ISOLA (pz) response files converter ---\n')
print('------------------------------------------------------------\n')

raw_yy = int(input('Insert a valid year of the event:\n'))
raw_mt = int(input('Insert a valid month of the event:\n'))
raw_dd = int(input('Insert a valid day of the event:\n'))
raw_hh = int(input('Insert a valid hour of the event:\n'))
raw_mm = int(input('Insert a valid minute of the event:\n'))
raw_ss = input('Insert a valid second of the event with 2 decimals in precision:\n')
raw_ext = input('Do you want last line of complex zeros to be extracted? (1 = Yes, 0 = No):\n')

raw_ss = raw_ss.split('.')
raw_ms = int(raw_ss[1])*10000
raw_ss = int(raw_ss[0])


#To know all available rdseed response files in CAL directory
files = np.asarray(os.listdir('./CAL/'))
files_n = []
for i in files:
	if 'RESP' in i:
		files_n.append(i)
files = np.asarray(files_n)

#Creating log file
f_log = open('log.txt','w')

for k in range(len(files)):
	#reading lines of the file
	f = open('./CAL/'+files[k],'r')
	l = np.asarray(f.readlines())

	#getting ranges of lines to find parameters
	mini, maxi = finding_ranges(l)

	if(mini != 'NO' and maxi != 'NO'):
		#getting parameters from ranged lines
		A0_val, inv_sens, n_zeros, n_poles, zeros, poles = extraction_data(mini, maxi, l)

		#Writting
		type0, cm, name, code, ch = files[k].split('.')
	
		#defining directory names and creating them
		main_dir = 'CAL_OUT'
		directory = str(raw_yy)+'_'+str(raw_mt)+'_'+str(raw_dd)+'_'+str(raw_hh)+'_'+str(raw_mm)+'_'+str(raw_ss)+'.'+str(raw_ms)
		if os.path.isdir('CAL_OUT') != True:
			os.mkdir(main_dir)

		path_out = './'+main_dir+'/'+directory

		if os.path.isdir(path_out) != True:
			os.mkdir(path_out)

		name_out = name+'B'+ch[1:]+'.pz'

		f_out = open(path_out+'/'+name_out,'w')
		f_out.write('A0\n'+
					A0_val+'\n'+
					'count-->m/sec\n'+
					inv_sens+'\n'+
					'zeroes\n'+
					n_zeros+'\n'
					)
		for j in range(len(zeros)):
			f_out.write(zeros[j,0]+'     '+zeros[j,1]+'\n')
		f_out.write('poles\n'+
	            	n_poles+'\n'
	           		)
		for j in range(len(poles)):
			f_out.write(poles[j,0]+'     '+poles[j,1]+'\n')
    
		f_out.close()

		f_log.write(files[k]+'   '+'Successful_converted'+'   '+name_out+'\n')

	else:
		#Log information in case that event is older than intrumentation installation
		f_log.write(files[k]+'   '+'Not_converted'+'   '+'NA'+'\n')
	
	f.close()

f_log.close()
print('Done!\n'+
	'You can find more information of which rdseed response files where converted and which ones not in log.txt file.\n'+
	'Please rememeber that the ones which were not converted was due event older age than the instrumentation installation.\n'+
	'Directory CAL_OUT contains another directiry named with the time of your event which contaisn all converted .pz files available.'
)





