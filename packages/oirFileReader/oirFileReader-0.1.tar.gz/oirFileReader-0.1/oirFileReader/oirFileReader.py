# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:02:00 2024

@author: Dominik Schneidereit
"""

import xmltodict
import flatdict
import numpy as np
import math


class OirFileReader:
    def __init__(self, filePath):
        f = open(filePath, 'rb')

        # for i in range(9):
        #      asd = f.read(16)
        #      print(asd)
        self.data = f.read()
        self.metaDataList = self.getImageMetadataList()

    def getImageMetadataList(self):
        data = self.data
        metaDataList = []
        xmlDataStart = 0
        rootName = b'lsmimage:imageProperties'
        xmlSearchString = b'<?xml version="1.0" encoding="ASCII"?>\r\n<'+rootName
        
    
        while (data.find(xmlSearchString, xmlDataStart))!= -1:
            
            xmlDataStart = data.find(xmlSearchString, xmlDataStart)
            
            xmlDataEnd = data.find(rootName, xmlDataStart+len(xmlSearchString)+1)+len(rootName)+1
                
            #print(xmlDataEnd-xmlDataStart)
                
            xmlData = data[xmlDataStart:xmlDataEnd]
                
                
            xmlDict = xmltodict.parse(xmlData)
            flatXmlDict = dict(flatdict.FlatDict(xmlDict))
            metaDataList.append(flatXmlDict)
            
            
            xmlDataStart += 10
        
        
        return metaDataList
    
    
    def getImageDimensionsFromMetadata(self):
        
        x = int(self.metaDataList[1].get('lsmimage:imageProperties:commonimage:imageInfo:commonimage:width'))
        y = int(self.metaDataList[1].get('lsmimage:imageProperties:commonimage:imageInfo:commonimage:height'))
        z = int(self.metaDataList[1].get('lsmimage:imageProperties:commonimage:imageInfo:commonimage:axis:commonparam:maxSize'))
        c = len(self.metaDataList[0].get('lsmimage:imageProperties:commonimage:acquisition:commonimage:imagingParam:lsmparam:pmt'))
        return (c,z,x,y)
    
    
    def getChannelIdsFromMetaData(self):
        
        channelInfos = self.metaDataList[0].get('lsmimage:imageProperties:commonimage:acquisition:commonimage:imagingParam:lsmparam:pmt')
        channelIds = []
    
        for element in channelInfos:
            channelIds.append(element.get('@channelId'))
        
        return channelIds
        
    def getImagePixels(self):
        data = self.data
        imageDimensions = self.getImageDimensionsFromMetadata()
        imagePixels = np.zeros((imageDimensions))
        channelIds = self.getChannelIdsFromMetaData()
        
        for c in range(imageDimensions[0]):
            bChannelId = channelIds[c].encode('ascii')
            startPointChunk = 0
            
            for z in range(imageDimensions[1]):
                    
                sliceData = np.zeros((imageDimensions[2],imageDimensions[3]))
                bSliceNumber = str(z+1).zfill(3).encode('ascii')
                searchBString = b'z'+ bSliceNumber +b'_0_1_'+bChannelId
                bytesPerPixel = 2
                nChunks = math.ceil(imageDimensions[2]/10)
                chunkPos = 0
        
                for i in range(nChunks):
                    startPointChunk = data.find(searchBString,startPointChunk)
                    startPointChunkSizeInfo = data.find(b'\x00',startPointChunk)
                    startPointData = startPointChunkSizeInfo+8
                    chunkSize = int.from_bytes(data[startPointChunkSizeInfo:startPointChunkSizeInfo+2], byteorder='little')
                    linesPerChunk = int(chunkSize/(bytesPerPixel*imageDimensions[2]))
                    #firstPixel = int.from_bytes(data[startPointData:startPointData+2], byteorder='little')
                    
                    #chunk = array.array('H',data[startPointData:startPointData+chunkSize])
                    chunk = np.frombuffer(data[startPointData:startPointData+chunkSize], np.uint16)
                    
                    reshapedChunk = chunk.reshape((int(chunkSize/(imageDimensions[2]*2)),imageDimensions[3]))
                    
                    #print(int(chunkSize/1024))
                    #print(np.size(reshapedChunk,0))
                    
                    for j in range(np.size(reshapedChunk,0)):
                        
                        sliceData[(j+chunkPos),:] = reshapedChunk[j,:]
                    
                    # print(data[startPointChunk:startPointChunkSizeInfo])
                    # print (chunkSize)
                    # print (firstPixel)
                    chunkPos += linesPerChunk
                    startPointChunk = startPointChunk+10
                
                imagePixels[c,z,:,:] = sliceData
            
        
        return imagePixels
    
   
