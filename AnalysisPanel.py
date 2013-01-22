#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.5 (standalone edition) on Mon Jan 07 18:13:42 2013

import wx
from Model.StockData import *
from Model.DataManager import *
import random
from util.draw import *
# begin wxGlade: extracode
# end wxGlade


class AnalysisPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AnalysisPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.Buffer = None
       
        self.__stockList = []
        quote = '002094'
        dm = DataManager()        
        q = dm.GetQuoteData(quote, 1800, 30)
        self.df = q.df
        for bar in xrange(len(q.close)):
            a = StockData(quote)
            a.open = q.open[bar]
            a.close = q.close[bar]
            a.high = q.high[bar]
            a.low = q.low[bar]
            self.__stockList.append(a)
        # end wxGlade
        
#        for i in range(100):
#            stock = StockData("")
#            stock.open = random.uniform(1.,100.)
#            stock.close = random.uniform(1.,100.)
#            stock.high = max(stock.open, stock.close) + random.uniform(1.,10.)
#            stock.low = min(stock.open, stock.close)- random.uniform(1.,10.)
#            self.__stockList.append(stock)
        

    def __set_properties(self):
        # begin wxGlade: AnalysisPanel.__set_properties
        self.SetSize((588, 422))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AnalysisPanel.__do_layout
        pass
        # end wxGlade
    def InitBuffer(self):
        size=self.GetClientSize()
        # if buffer exists and size hasn't changed do nothing
        if self.Buffer is not None and self.Buffer.GetWidth() == size.width and self.Buffer.GetHeight() == size.height:
            return False
        
        self.Buffer=wx.EmptyBitmap(size.width,size.height)
        dc=wx.MemoryDC()
        #dc = wx.ClientDC()
        dc.SelectObject(self.Buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()    
        
        #self.DrawCandleLineList(dc, self.__stockList)
        draw_candle(dc, self.df)
        dc.SelectObject(wx.NullBitmap)
        return True

    def __getStockDataListRange(self, stockdataList):
        highlist = [s.high for s in stockdataList]
        lowlist = [s.low for s in stockdataList]
        return (min(lowlist), max(highlist))
    
    def DrawCandleLineList(self, dc, stockdataList):
                                
        size=self.GetClientSize()         
        windowWidth = size.width-10
        windowHeight = size.height-10
        dc.SetDeviceOrigin(0, windowHeight)
        dc.SetAxisOrientation(True, True)

        stockRange = self.__getStockDataListRange(stockdataList)
        recwidth = float(windowWidth)/len(stockdataList)
        for i in range(len(stockdataList)):
            stock = stockdataList[i]
            pricediff = stockRange[1] - stockRange[0]
            recheight = windowHeight*abs(stock.close - stock.open)/pricediff+1
            x = i*windowWidth/len(stockdataList)+1
            upperlineendY = (stock.high - stockRange[0])*windowHeight/pricediff                 
            lowerlineendY = (stock.low - stockRange[0])*windowHeight/pricediff
            drop = False
            if stock.close >= stock.open:                 
                y = upperlineendY - (stock.high - stock.open)*windowHeight/pricediff       
            else:                
                drop = True             
                y = upperlineendY - (stock.high - stock.close)*windowHeight/pricediff  
                   
            rec = (x, y, recwidth, recheight)
            upperline = (x+recwidth/2, y+recheight, x+recwidth/2, upperlineendY)
            lowerline = (x+recwidth/2, y, x+recwidth/2, lowerlineendY)
           
            if drop:
                dc.SetBrush(wx.BLACK_BRUSH)
            else:                
                dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(rec[0], rec[1], rec[2], rec[3])
            dc.DrawLine(upperline[0], upperline[1], upperline[2], upperline[3])
            dc.DrawLine(lowerline[0], lowerline[1], lowerline[2], lowerline[3])
            


    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker

    def OnPaint(self, event):
        if self.InitBuffer():
            self.Refresh() # buffer changed paint in next event, this paint event may be old
            return
        
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.Buffer, 0, 0)
        
        draw_candle(dc, self.df)
        #self.DrawCandleLineList(dc, self.__stockList)
        

# end of class AnalysisPanel