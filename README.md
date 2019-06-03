# rdseed2pz
Code for converting rdseed instrument response format to .pz for ISOLA Matlab GUI use.

-- Use & Requirements --:

- Before use, please check you meet the requirements for a success execution of the code. These were the specifictions used to write the code:

    + Python 3.6.7
    + Python Libraries: datetime 4.3, numpy 1.16.3, os (normally comes with Python 3, not need to be installed).
      NOTE: In case you don't have one of these libraries, install them with pip3:
      
          "pip3 install -name_of_library-"

- The code is made to be run on Python 3. You need first to move all rdseed or SEED response files format in a directory called "CAL" aside with the python code "rdseed2pz.py".

- Once you had everything in order, run the code with Python 3 in the terminal:

    "python3 rdseed2pz.py"
      
NOTE: 
Every rdseed or seed response file has its own data according to the entries. This means that the file register every change to instrumentation by date, its time opeating in that way, and thus, the specifications and values will change according to dates, but the file will save these details with the dates.
The code will ask you for the specific date of an event in order to extract some values which where the ones operating during the event (valid during the date of the event). These specifications (the following) are taken to be use mainly with ISOLA Matlab GUI code:
    + Normalization factor.
    + Inverse of channel sensitivity.
    + Numbers of Complex Zeros and Complex Poles.
    + Values of Complex Zeros and Complex Poles (two columns each, real and imaginary values).
    
- After input of the date of event, interface will ask you if you want the last line of Complex Zeros in the new .pz files to be removed (one real and one imaginary, the last).

- The output can be found in a directory created by the code called "CAL_OUT", where inside is another directory named with the specification of the event, which finally contains all the .pz response files for ISOLA use. This organization is the output since maybe the user want to continue using the code with another event. In that case, another directory with a name of the new event, aside with the old one, will be found in the same main output directory ("CAL_OUT").
