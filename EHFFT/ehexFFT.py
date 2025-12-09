import torch
import numpy as np

def hexUpDiag(n):
  return [np.floor((n+1)*0.5).astype(int),np.floor(n).astype(int)]

def hexDownDiag(n):
  return [np.floor(-(n+1)*0.5).astype(int),np.floor(n).astype(int)]

def hexFreq(mat):
  freqDiagUp = torch.zeros(mat.shape)
  freqDiagDown = torch.zeros(mat.shape)
  freqVert = torch.zeros(mat.shape)
  freqs = torch.fft.fftfreq(2*mat.shape[1])
  for i in range(mat.shape[0]//2):
    for j in range(2*mat.shape[1]):
      ptsUpX = (i+hexUpDiag(j)[0])%mat.shape[0]
      ptsUpY = (hexUpDiag(j)[1])%mat.shape[1]
      ptsDownX = (i+hexDownDiag(j)[0])%mat.shape[0]
      ptsDownY = (hexDownDiag(j)[1])%mat.shape[1]
      freqDiagUp[ptsUpX,ptsUpY] = freqs[j]
      freqDiagDown[ptsDownX,ptsDownY] = freqs[j]
    freqVert[:,i] = torch.fft.fftfreq(mat.shape[1])
  return freqVert, freqDiagUp, freqDiagDown

def hexFFT(mat):
  diagUp = torch.zeros(mat.shape,dtype=torch.complex64)
  diagDown = torch.zeros(mat.shape,dtype=torch.complex64)
  vert = torch.zeros(mat.shape,dtype=torch.complex64)

  supportTensor = torch.zeros(2*mat.shape[1])

  for i in range(mat.shape[0]//2):
    for j in range(2*mat.shape[1]):
      ptsUpX = (i+hexUpDiag(j)[0])%mat.shape[0]
      ptsUpY = (hexUpDiag(j)[1])%mat.shape[1]
      supportTensor[j] = mat[ptsUpX,ptsUpY]

    supportTensor = torch.fft.fft(supportTensor)
    for j in range(2*mat.shape[1]):
      ptsUpX = (i+hexUpDiag(j)[0])%mat.shape[0]
      ptsUpY = (hexUpDiag(j)[1])%mat.shape[1]
      diagUp[ptsUpX,ptsUpY] = supportTensor[j]

    for j in range(2*mat.shape[1]):
      ptsDownX = (i+hexDownDiag(j)[0])%mat.shape[0]
      ptsDownY = (hexDownDiag(j)[1])%mat.shape[1]
      supportTensor[j] = mat[ptsDownX,ptsDownY]
    supportTensor = torch.fft.fft(supportTensor)
    for j in range(2*mat.shape[1]):
      ptsDownX = (i+hexDownDiag(j)[0])%mat.shape[0]
      ptsDownY = (hexDownDiag(j)[1])%mat.shape[1]
      diagDown[ptsDownX,ptsDownY] = supportTensor[j]
  for i in range(mat.shape[0]):
    vert[:,i] = torch.fft.fft(mat[:,i].clone())
  return vert, diagUp, diagDown

def hexIFFT(vert, diagUp, diagDown,kernel=[.5,.25,.25]):
  diagUpIFT = torch.zeros(vert.shape,dtype=torch.complex64)
  diagDownIFT = torch.zeros(vert.shape,dtype=torch.complex64)
  vertIFT = torch.zeros(vert.shape,dtype=torch.complex64)

  supportTensor = torch.zeros(2*vert.shape[1])
  for i in range(diagUp.shape[0]//2):
    for j in range(2*diagUp.shape[1]):
      ptsUpX = (i+hexUpDiag(j)[0])%diagUp.shape[0]
      ptsUpY = (hexUpDiag(j)[1])%diagUp.shape[1]
      supportTensor[j] = diagUp[ptsUpX,ptsUpY]
    supportTensor = torch.fft.ifft(supportTensor)

    for j in range(2*diagUp.shape[1]):
      ptsUpX = (i+hexUpDiag(j)[0])%diagUp.shape[0]
      ptsUpY = (hexUpDiag(j)[1])%diagUp.shape[1]
      diagUpIFT[ptsUpX,ptsUpY] = supportTensor[j]

    for j in range(2*diagUp.shape[1]):
      ptsDownX = (i+hexDownDiag(j)[0])%diagUp.shape[0]
      ptsDownY = (hexDownDiag(j)[1])%diagUp.shape[1]
      supportTensor[j] = diagDown[ptsDownX,ptsDownY]
    supportTensor = torch.fft.ifft(supportTensor)
    for j in range(2*diagDown.shape[1]):
      ptsDownX = (i+hexDownDiag(j)[0])%diagDown.shape[0]
      ptsDownY = (hexDownDiag(j)[1])%diagDown.shape[1]
      diagDownIFT[ptsDownX,ptsDownY] = supportTensor[j]

  for i in range(diagUp.shape[0]):
    vertIFT[:,i] = torch.fft.ifft(vert[:,i])
  if kernel is None:
    return vertIFT, diagUpIFT, diagDownIFT
  else:
    return kernel[0]*vertIFT+kernel[1]*diagUpIFT+kernel[2]*diagDownIFT

