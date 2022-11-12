from tkinter import HIDDEN
import streamlit as st
import streamlit_vertical_slider as svs
import pandas as pd
import functions as fn
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.fft import irfft
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import plotly_express as px
import IPython.display as ipd
import librosa
import altair as alt
import animation as animation
import time
import plotly.graph_objects as go
#------------ Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ----------------------- Main Window Elements --------------------------- #
# normalIndex=[] 
# numofPoints=0
# magnitude_n=[]


# # ------------------
# magnitude=[]
# freq=[] 
# numPoints_1=0 
# startIndex_1=0
# numPoints_2=0 
# startIndex_2=0
# numPoints_3=0 
# startIndex_3=0
# numPoints_4=0 
# startIndex_4=0
# samplfreq=0

normalIndex=[] 
numofPoints=0
magnitude_n=[]

# sliders = []
# ------------------
magnitude=[]
freq=[] 
numpoints = []
startIndex =[]
samplfreq=0
lines1=any
file_uploaded = st.sidebar.file_uploader("")

radio_button = st.sidebar.radio("", ["Normal", "Music", "Vowels", "Medical","Optional"], horizontal=False)



if file_uploaded==None:
    welcome_text = '<p class="page_titel", style="font-family:Arial">Please upload file </p>'
    st.markdown(welcome_text, unsafe_allow_html=True)

else:
    if radio_button == "Music" or radio_button == "Normal" or radio_button == "Vowels":
        signal_x_axis_before, signal_y_axis_before, sample_rate_before ,sound_info_before = animation.read_audio(file_uploaded)
        df = pd.DataFrame({'time': signal_x_axis_before[::500], 'amplitude': signal_y_axis_before[:: 500]}, columns=['time', 'amplitude'])
        lines = alt.Chart(df).mark_line().encode( x=alt.X('0:T', axis=alt.Axis(title='time')),
                                                y=alt.Y('1:Q', axis=alt.Axis(title='amplitude'))).properties(width=500,height=250)
        samplfreq , audio = wavfile.read(file_uploaded.name)  
        if radio_button == "Normal":
            # slider min and max 
            names_list = [(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0, 5,1),(0,5,1)]
            # slider labels
            label= ["1kHz","2kHz","3kHz","4kHz","5kHz","6kHz","7kHz","8kHz","9kHz","10kHz"]
            # read file          
            sliders =fn.creating_sliders(names_list,label)
            audio = audio[:200000]
            magnitude , freq_n=fn.fourierTansformWave(audio ,samplfreq)   # convert to fft
            normalIndex , numofPoints =fn.bandLength(freq_n)  # get index of slider in how point will change when move slider 
            for i in range(10):
                if i<9: 
                    numpoints.append(int(numofPoints/2))
                else:
                    numofPoints=(numofPoints/2)*9 +numofPoints
                startIndex.append(int(normalIndex[i]/2))
            print("This is ",numofPoints)
            numpoints = int(numofPoints)
#------------------------------------ MUSIC -----------------------------------------

        elif radio_button == "Music":
            names_list = [(0,5,1),(0,5,1),(0,5,1),(0,5,1)]
            label= [" Drums","base guitar" , "piano" ,"guitar"]
                #audio = audio[:200000]
            sliders =fn.creating_sliders(names_list,label)
            magnitude , freq=fn.fourierTansformWave(audio ,samplfreq)   # convert to fft
            points_per_freq = np.ceil(len(freq) / (samplfreq / 2) )  # number of points per  frequancy 
            points_per_freq = int(points_per_freq)
            frequencies = [0, 500, 1000, 2000, 5000]
            for i in range(len(label)):
                    numpoints.insert(i,np.abs(frequencies[i] * points_per_freq - frequencies[i+1] * points_per_freq))
                    startIndex.insert(i,frequencies[i] * points_per_freq)
            

    # ------------------------------------------------- END MUSIC  ----------------------------------


        elif radio_button == "Vowels":
            names_list = [(20,30,25),(20,30,25)]
            label= ["0:100","100:200"]
            sliders =fn.creating_sliders(names_list,label)
        
        magnitude=fn.modify_wave(magnitude , numpoints , startIndex , sliders, len(label))         
        new_sig = irfft(magnitude)
        norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
        write("convertWave4.wav", samplfreq, norm_new_sig)
        signal_x_axis_after, signal_y_axis_after, sample_rate_after ,sound_info_after = animation.read_audio("convertWave4.wav")    # Read Audio File
        df1 = pd.DataFrame({'time': signal_x_axis_after[::500], 'amplitude': signal_y_axis_after[:: 500]}, columns=['time', 'amplitude'])
        lines1 = alt.Chart(df).mark_line().encode( x=alt.X('0:T', axis=alt.Axis(title='time')),
                                                y=alt.Y('1:Q', axis=alt.Axis(title='amplitude'))).properties(width=500,height=250)

        fig1 = plt.figure(figsize=(5, 2))
        plt.specgram(new_sig, Fs=samplfreq, vmin=-20, vmax=50)
        plt.colorbar()
        start_btn_col ,stop_btn_col =st.sidebar.columns(2)
        with start_btn_col:
            start_btn = st.button('Start') 
        with stop_btn_col:
            stop_btn =st.button('stop')
        # Plot Animation
        before_col,after_col=st.columns(2)
        with before_col:
            st.write("before")
            line_plot_before = st.altair_chart(lines)
            st.audio(file_uploaded)
        with after_col:
            st.write("after")
            line_plot_after= st.altair_chart(lines1)
            st.audio("convertWave4.wav" )
            st.pyplot(fig1)
       
        
      
            
    elif radio_button == "Medical":
        names_list = [(0,10,1)]
        label= ["0:10"]
        sliders =fn.creating_sliders(names_list,label)


    N = df.shape[0]  # number of elements in the dataframe
    burst = 6        # number of elements (months) to add to the plot
    size = burst         # size of the current dataset 
    if start_btn:
        for i in range(1, N):
            step_df  = df.iloc[0:size]
            step_df1 = df1.iloc[0:size]

            lines  = animation.plot_animation(step_df)
            lines1 = animation.plot_animation(step_df1)


            line_plot_befor  = line_plot_before.altair_chart(lines)
            line_plot_after= line_plot_after.altair_chart(lines1)

            size = i + burst
            if size >= N:
                size = N - 1
            time.sleep(.00000000001)
            if stop_btn:
                break
