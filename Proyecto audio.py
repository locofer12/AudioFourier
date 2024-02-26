import scipy.fftpack as fourier 
import matplotlib.pyplot as plt 
import pyaudio as PyAu    
import numpy as np               
import struct                    # datos hexadecimales a decimales

fps = 1024*10                 #datos de frecuencia totales
Formato = PyAu.paInt16             #se toman 16 bits 
Fs = 44100                       #Frecuencia para el audio
Fmin = 20                 #Frecuencia minima es 20 porque es la menor a la que el humano puede escuchar
Fmax = 20000              #Frecuencia máxima no mayor 20k (max rango de audioción humana)

p = PyAu.PyAudio()                 #con ello se configura el audio . 

Stream = p.open(format = Formato, channels = 1, rate = Fs, input = True, 
                output = True, frames_per_buffer = fps)

fig, (ax,ax1) = plt.subplots(2)

x_audio = np.arange(0,fps,1)  #datos fps de uno en uno

x_fft = np.linspace(0, Fs, fps) #cantidad muestras para transformada de fourier

ln, = ax.plot(x_audio, np.zeros(fps),'chocolate')#se crean valores con ceros de porque se actializaran

ln_fft, = ax1.semilogx(x_fft, np.zeros(fps), 'salmon',base = 2)      #se crean valores con ceros de igual forma porque se actualizaran

ax.set_ylim(-10000,10000) #Limite de y para datos del microfono                                                    
ax.set_xlim(0,fps//10) #Limite de gráfica (10% de los datos tomados por segundo)

ax1.set_xlim(Fmin,Fmax)   #Se configuran valores en la gráfica

fig.show()

F = (Fs/fps)*np.arange(0,fps//2) #Rango de frecuencias

while True:
    
    #Leemos paquetes de longitud fps
    data = Stream.read(fps)  #bytes                      
    #Convertimos los datos que se encuentran empaquetados en hexadecimales a decimal entero
    dataInt = struct.unpack(str(fps) + 'h', data)   
    
    ln.set_ydata(dataInt) #Asignamos los datos a la curva de la variación temporal
    
    #Calculamos la transformada de fourier y la Magnitud de la FFTtransformada del paqute de datos
    VP = abs(fourier.fft(dataInt)/fps) #para evitar que los datos no se vayan a valores enormes(VP=valores pequeños)
    #Con esto calculamos la Amplitud

    #El tamaño de la respuesta en frecuencia en el eje y depende del valor más alto registrado
    ax1.set_ylim(0,np.max(VP+20)) #20 es espacio          
    #Asigmanos la Magnitud de la transformada a la curva del espectro 
    ln_fft.set_ydata(VP) 
    
    #Tomamos la mitad del espectro para encontrar la Frecuencia Dominante
    VP = VP[0:fps//2] #toma el intervalo de interes                      
    
    mmaxx = np.where(VP == np.max(VP)) #Comparacion de los datos a encontrar cual dato es mas grande 
    #indica la posicion maxima de la lista VP
    
    #Encontramos la frecuencia que corresponde con el máximo de VP
    FreqDom = F[mmaxx]  #Frecuencia      
    
    #se muestra el valor de la frecuencia 
    ax.set_title("Frecuencia: " +str(int(FreqDom)) + " en Hz")
   
    try: 
        fig.canvas.draw() #actualizar (renovando la grafica)
        fig.canvas.flush_events() # actualizar la grafica
    except:
        break
    