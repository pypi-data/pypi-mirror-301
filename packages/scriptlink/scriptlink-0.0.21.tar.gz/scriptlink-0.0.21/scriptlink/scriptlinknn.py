###############NN Classes#############

from scriptlink import *
import numpy as np
import platform
class LetterModel():
    def __init__(self,modelname="SimpleNN2Layer"):
        datadirectory="models\\"
        if (modelname=="SimpleNN3Layer"):
            self.nn=SimpleNN3Layer()
            modelfilename=datadirectory+"weights3.npy"
        if (modelname=="SimpleNN2Layer"):
            self.nn=SimpleNN2Layer()
            modelfilename=datadirectory+"weights2.npy"
        if (modelname=="SimpleConv"):
            self.nn=SimpleConvLayer()
            modelfilename=datadirectory+"weightsconv.npy"
        answers=36
        self.nn.LoadModel(modelfilename=modelfilename,clear=False,hhlayersz=72,answers=answers)
        self.nn.SetParams(desiredacc=.80,alpha=.1,iterations=100)
        print("SetParams(desiredacc=.80,alpha=.1,iterations=100)","modelfilename",modelfilename)
    def readtext(self,filename):
        if (type(filename)==type("")):
            from PIL import ImageTk, Image
            im = Image.open(filename)
            p = np.array(im)
        else:p=filename
        print(p.shape)
        newp=p[:28,:28,:1]
        return
        return self.nn.make_predictions(p)
        
        #main.nn.LoadDataFiles(trainfilename= trainfilename,testfilename=testfilename)
        #print("dataloaded")
        #answers=main.nn.GetMaxY()
        #hhct=answers*2
        #main.nn.LoadModel(modelfilename=modelfilename,clear=False,hhlayersz=hhct,answers=answers)
        #modelfilename=datafile+"weights2.npy"
    
class NNUtils():
    def logtext(text):
        cd.logtext(text.encode('utf8'))
    def loadcsv(filename, shape=(0,0),delimiter=ord(','), skiprows=0, dtype=int):
        if (shape==(0,0)):
            _datashape=(ctypes.c_int32 * 2)()
            rows=cd.GetLinesCsv(filename.encode('utf8'),_datashape,delimiter,skiprows=0)
            shape=(_datashape[0],_datashape[1])
        #print(shape)
        c_dtype=np.ctypeslib.as_ctypes_type(dtype)
        sz=np.prod(shape[0]*shape[1])
        #print(c_dtype,sz)
        _data=(c_dtype * sz)()
        #LoadCsv(char* str, int* returnbuf, int delimiter, int rows,int columns,int dtype, int skiprows)
        dtypename=ord('i')
        if (dtype==float):dtypename=ord('f')
        rows=cd.LoadCsv(filename.encode('utf8'),_data,delimiter,shape[1],dtypename,1)
        frame = np.ctypeslib.as_array(_data)
        frame=np.reshape(frame,shape)
        return frame
    def randomstring(le):
        cd.RandomString.restype = ctypes.c_char_p
        string=cd.RandomString(le).decode('utf-8')
        return string
class SimpleNN:
    def ReLU(Z):
        return np.maximum(Z, 0)

    def softmax(Z):
        A = np.exp(Z) / sum(np.exp(Z))
        return A
    def ReLU_deriv(Z):
        return Z > 0
    def one_hot(Y):#(59000)
        one_hot_Y = np.zeros((Y.size, Y.max() + 1))#(59000,11)
        one_hot_Y[np.arange(Y.size), Y] = 1        #(59000,11) ones set
        one_hot_Y = one_hot_Y.T                    #(11,59000) transpose
        return one_hot_Y                           #(11,59000) 
    
    
    def SetParams(self,desiredacc=.75,alpha=.1,iterations=100):
        self.desiredacc=desiredacc
        self.alpha=alpha
        self.iterations=iterations
    def SaveModel(self):
        np.save(self.modelfilename,np.array(self.WandB, dtype=object), allow_pickle=True)
        print(self.modelfilename,"saved")
    def LoadData(self,train,test):
        if (type(train)==type("")):
            self.traindata = np.array(pd.read_csv(train))
        elif (isinstance(test, (np.ndarray, np.generic) )):
            self.traindata = train
        if (type(test)==type("")):
            self.testdata = np.array(pd.read_csv(test))
        elif (isinstance(test, (np.ndarray, np.generic) )):
            self.testdata = test
    def LoadDataFiles(self,trainshape=(0,0),trainfilename="",testshape=(0,0),testfilename=""):
        if (self.windows):
            self.traindata = np.array(WindowsUtils.loadcsvsl(trainfilename, shape=trainshape, skiprows=1,delimiter=ord(','),dtype=int))
            self.testdata = np.array(WindowsUtils.loadcsvsl(testfilename, shape=testshape, skiprows=1,delimiter=ord(','),dtype=int))
        else:
            self.traindata = np.loadtxt(trainfilename, skiprows=1,delimiter=ord(','),dtype=int)
            self.testdata = np.loadtxt(testfilename, skiprows=1,delimiter=ord(','),dtype=int)
    def LoadDataFilesPandas(self,trainfilename,testfilename):
        self.traindata = np.array(pd.read_csv(trainfilename))
        self.testdata = np.array(pd.read_csv(testfilename))
    def LoadDataFromArray(self,train,test):
        self.traindata = train
        self.testdata = test
    def GetMaxY(self):
        Y = self.traindata.T[0]#(785,59000)
        return Y.max()+1
        #self.Y_train = data[0]#(59000)
    def LoadUbyteDataFiles(path, kind='train'):
        kind='train'
        """Load MNIST data from `path`"""
        labels_path = os.path.join(path, '%s-labels.idx1-ubyte' % kind)
        images_path = os.path.join(path, '%s-images.idx3-ubyte' % kind)
        with open(labels_path, 'rb') as lbpath:
            magic, n = struct.unpack('>II', lbpath.read(8))
            labels = np.fromfile(lbpath, dtype=np.uint8)
        with open(images_path, 'rb') as imgpath:
            magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
            images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
        
    def getaccuracyofmodel(self):
        tm=0
        for i in range(10):
            np.random.shuffle(self.testdata)
            data_dev = self.testdata[0:5000].T
            Y_dev = data_dev[0]
            X_dev = data_dev[1:]
            X_dev = X_dev / 255.
            ck=clock()
            dev_predictions = self.make_predictions(X_dev)
            tm+=clock()-ck
            a=self.get_accuracy(dev_predictions, Y_dev)
            print("gradient_descent(mnist_test.csv, 0.10, 100) accuracy:%.2f time %d: "%(a,tm),X_dev.shape,Y_dev.shape)
        return a
    def trainmodelwith_gd(self):
        ck=clock();
        while(1):
            np.random.shuffle(self.traindata)
            rows, cols = self.traindata.shape
            #m, n = data.shape
            shape=self.traindata.shape
            data = self.traindata[0:rows].T#(785,59000)
            self.Y_train = data[0]#(59000)
            self.X_train = data[1:cols]#(784,59000)
            self.X_train = self.X_train / 255.
            _,self.m_train = self.X_train.shape#59000'''
            
            print("self.X_train.shape",self.X_train.shape, " self.Y_train.shape",self.Y_train.shape,"Time:%d"%(clock()))
            #W1, b1, W2, b2,W3, b3 = self.gradient_descent(self.X_train, self.Y_train,0.10, 100,rows)    
            self.WandB = list(self.gradient_descent(self.X_train, self.Y_train,0.10, 100,rows))    
            #self.WandB=[W1, b1, W2, b2,W3, b3]
            #np.save("simplemnistweights.npy",np.array(W, dtype=object), allow_pickle=True)
            acc=self.getaccuracyofmodel()
            self.acc=acc
            if (self.acc>self.desiredacc):
                print("Time:%d"%(clock()-ck))
                break
    

    def findfailed(self):
        print("finding errorimg")
        #W1, b1, W2, b2,W3, b3 = self.WandB
        np.random.shuffle(self.traindata)
        rows, cols = self.traindata.shape
        #m, n = data.shape
        shape=self.traindata.shape
        data = self.traindata[0:rows].T#(785,59000)
        self.Y_train = data[0]#(59000)
        self.X_train = data[1:cols]#(784,59000)
        print(self.X_train[0][0],type(self.X_train[0][0]),self.X_train.shape)
        self.X_train = self.X_train / 255.
        _,self.m_train = self.X_train.shape#59000'''
        from matplotlib import pyplot as plt
        ck=clock()
        for index in range (10000):
            current_image = self.X_train[:, index, None]
            #print(current_image.shape)
            prediction = self.make_predictions(self.X_train[:, index, None])
            label = self.Y_train[index]
            if (prediction!=label):
                print("found %d time:%d"%(index,clock()-ck))
                print("Prediction: ", prediction)
                print("Label: ", label)
                '''filt=np.zeros((3,3),dtype=np.float64)
                filt[1][:]=1
                current_imageconv=Numps.convdll(current_image.reshape((28, 28)),filt)
                print(current_image.dtype)
                current_imageconv = current_imageconv.reshape((26, 26)) * 255
                plt.gray()
                plt.title("pred:%d actual:%d"%(prediction,label))
                plt.imshow(current_imageconv, interpolation='nearest')
                plt.show()'''
                print(current_image.shape,type(current_image[0][0]),current_image[0][0])
                current_image = current_image.reshape((28, 28)) * 255
                plt.gray()
                plt.title("pred:%d actual:%d"%(prediction,label))
                plt.imshow(current_image, interpolation='nearest')
                plt.show()
                yield index    




    def printlayershapes(layers):
        prev=(784,1)
        tot=0
        for ind in range(0,len(layers),2):
            i=layers[ind]
            print(i.shape)
            ops=i.shape[1]*i.shape[0]
            print("operations",ops)
            tot+=ops
            prev=i.shape
        print(tot)
        
        
class SimpleNN3Layer(SimpleNN):
    def __init__(self):
        self.windows= (platform.system() == "Windows")
        self.acc=0
    def LoadModel(self,modelfilename,clear=False,hhlayersz=20,answers=10):
        self.modelfilename=modelfilename
        self.answers=answers
        self.WandB=[]
        if (clear==False):
                try :
                    self.WandB=np.load(modelfilename,allow_pickle=True)
                except FileNotFoundError:
                    print("no weights file,clearing")
                    clear=True
        if (clear==True):
            self.WandB=[]
            hhlayersz=20
            W1 = np.random.rand(hhlayersz, 784) - 0.5
            b1 = np.random.rand(hhlayersz, 1) - 0.5
            W2 = np.random.rand(hhlayersz, hhlayersz) - 0.5
            b2 = np.random.rand(hhlayersz, 1) - 0.5
            W3 = np.random.rand(answers, hhlayersz) - 0.5
            b3 = np.random.rand(answers, 1) - 0.5
            self.WandB=[W1, b1, W2, b2,W3, b3,]
        SimpleNN.printlayershapes(self.WandB)
    
    
    
    def forward_prop(self,W1, b1, W2, b2,W3, b3, X):#(784,59000)
        Z1 = W1.dot(X) + b1
        A1 = SimpleNN.ReLU(Z1)
        Z2 = W2.dot(A1) + b2
        A2 = SimpleNN.ReLU(Z2)
        Z3 = W3.dot(A2) + b3
        A3 = SimpleNN.softmax(Z3)
        return Z1, A1, Z2, A2 , Z3, A3   
    def backward_prop(self,Z1, A1, Z2, A2,Z3, A3, W1, W2, W3,X, Y,m):#(784,59000)(59000)    
        one_hot_Y = SimpleNN.one_hot(Y)
        dZ3 = A3 - one_hot_Y
        dW3 = 1 / m * dZ3.dot(A2.T)
        db3 = 1 / m * np.sum(dZ3)
        dZ2 = W3.T.dot(dZ3) * SimpleNN.ReLU_deriv(Z2)
        dW2 =  1 / m * dZ2.dot(A1.T)
        db2 = 1 / m * np.sum(dZ2)
        dZ1 = W2.T.dot(dZ2) * SimpleNN.ReLU_deriv(Z1)
        dW1 = 1 / m * dZ1.dot(X.T)
        db1 = 1 / m * np.sum(dZ1)
        return dW1, db1, dW2, db2,dW3, db3
    def update_params(self,W1, b1, W2, b2,W3, b3, dW1, db1, dW2, db2,dW3, db3, alpha):
        W1 = W1 - alpha * dW1
        b1 = b1 - alpha * db1    
        W2 = W2 - alpha * dW2  
        b2 = b2 - alpha * db2    
        W3 = W3 - alpha * dW3  
        b3 = b3 - alpha * db3    
        return W1, b1, W2, b2,W3, b3
        
        
        
    def get_predictions(self,A2):
        return np.argmax(A2, 0)
    def get_accuracy(self,predictions, Y):
        #print(predictions, Y)
        return np.sum(predictions == Y) / Y.size
    def make_predictions(self,X):
        W1, b1, W2, b2,W3, b3=self.WandB
        _, _, _,_, _, A2 = self.forward_prop(W1, b1, W2, b2, W3, b3, X)
        predictions = self.get_predictions(A2)
        return predictions
    
    
    
    def gradient_descent(self,X, Y, alpha, iterations,rows,):#self.X_train, self.Y_train, 0.10, 100) 
        
        W1, b1, W2, b2,W3, b3=self.WandB
        
        for i in range(iterations):
            Z1, A1, Z2, A2, Z3, A3 = self.forward_prop(W1, b1, W2, b2,W3, b3, X)
            dW1, db1, dW2, db2,dW3, db3 = self.backward_prop(Z1, A1, Z2, A2,Z3, A3, W1, W2,W3, X, Y,rows)
            W1, b1, W2, b2, W3, b3 = self.update_params(W1, b1, W2, b2,W3, b3, dW1, db1, dW2, db2,dW3, db3, alpha)
            if i % 10 == 0:
                print("Iteration: ", i)
                predictions = self.get_predictions(A3)
                print(self.get_accuracy(predictions, Y))
        return W1, b1, W2, b2,W3, b3
    
    
    
    
    

class SimpleNN2Layer(SimpleNN):
    def __init__(self):
        self.windows= (platform.system() == "Windows")
        self.acc=0
    def LoadModel(self,modelfilename,clear=False,hhlayersz=20,answers=10):
        self.modelfilename=modelfilename
        self.answers=answers
        self.WandB=[]
        if (clear==False):
                try :
                    self.WandB=np.load(modelfilename,allow_pickle=True)
                except FileNotFoundError:
                    print("no weights file,clearing")
                    clear=True
        if (clear==True):
            self.WandB=[]
            hhlayersz=20
            W1 = np.random.rand(hhlayersz, 784) - 0.5
            b1 = np.random.rand(hhlayersz, 1) - 0.5
            W2 = np.random.rand(answers, hhlayersz) - 0.5
            b2 = np.random.rand(answers, 1) - 0.5
            self.WandB=[W1, b1, W2, b2]
        SimpleNN.printlayershapes(self.WandB)
        
    def forward_prop(self,W1, b1, W2, b2, X):#(784,59000)
        Z1 = W1.dot(X) + b1
        A1 = SimpleNN2Layer.ReLU(Z1)
        Z2 = W2.dot(A1) + b2
        A2 = SimpleNN2Layer.softmax(Z2)
        return Z1, A1, Z2, A2    

   
        
    def backward_prop(self,Z1, A1, Z2, A2, W1, W2, X, Y,m):#(784,59000)(59000)    
        one_hot_Y = SimpleNN2Layer.one_hot(Y)
        dZ2 = A2 - one_hot_Y
        dW2 = 1 / m * dZ2.dot(A1.T)
        db2 = 1 / m * np.sum(dZ2)
        dZ1 = W2.T.dot(dZ2) * SimpleNN2Layer.ReLU_deriv(Z1)
        dW1 = 1 / m * dZ1.dot(X.T)
        db1 = 1 / m * np.sum(dZ1)
        return dW1, db1, dW2, db2
    def update_params(self,W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
        W1 = W1 - alpha * dW1
        b1 = b1 - alpha * db1    
        W2 = W2 - alpha * dW2  
        b2 = b2 - alpha * db2    
        return W1, b1, W2, b2
        
        
        
    def get_predictions(self,A2):
        return np.argmax(A2, 0)
    def get_accuracy(self,predictions, Y):
        #print(predictions, Y)
        return np.sum(predictions == Y) / Y.size
    def make_predictions(self,X):
        W1, b1, W2, b2=self.WandB
        _, _, _, A2 = self.forward_prop(W1, b1, W2, b2, X)
        predictions = self.get_predictions(A2)
        return predictions
    
    
    
    def gradient_descent(self,X, Y, alpha, iterations,rows):#self.X_train, self.Y_train, 0.10, 100) 
        W1, b1, W2, b2 = self.WandB
        forck=0
        backck=0
        for i in range(iterations):
            ck=time.time()
            Z1, A1, Z2, A2 = self.forward_prop(W1, b1, W2, b2, X)
            forck+=time.time()-ck
            ck=time.time()
            dW1, db1, dW2, db2 = self.backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y,rows)
            backck+=time.time()-ck
            ck=time.time()
            W1, b1, W2, b2 = self.update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
            if i % 10 == 0:
                print("Iteration: %d for:%.2f bk:%.2f"%( i,forck,backck))
                predictions = self.get_predictions(A2)
                print(self.get_accuracy(predictions, Y))
        return W1, b1, W2, b2
class torchconv():
    def __init__(self):
        pass
class SimpleConv(SimpleNN):
    def __init__(self):
        self.windows= (platform.system() == "Windows")
        self.acc=0
    def LoadModel(self,modelfilename,clear=False,hhlayersz=20):
        self.modelfilename=modelfilename
        self.WandB=[]
        if (clear==False):
                try :
                    self.WandB=np.load(modelfilename,allow_pickle=True)
                except FileNotFoundError:
                    print("no weights file,clearing")
                    clear=True
                except:
                    print("unknown error")
        if (clear==True):
            self.WandB=[]
            hhlayersz=20
            W0=(np.random.rand(5, 5,  6) - 0.5) * 0.2 # random sample in [-0.1, 0.1] 
            b0=(np.random.rand(1, 1,  6) - 0.5) * 0.2 # random sample in [-0.1, 0.1] 
            W1 = np.random.rand(hhlayersz, 784) - 0.5
            b1 = np.random.rand(hhlayersz, 1) - 0.5
            W2 = np.random.rand(10, hhlayersz) - 0.5
            b2 = np.random.rand(10, 1) - 0.5
            self.WandB=[W1, b1, W2, b2]
            '''f = layer['f']
            n_C = layer['n_C']
            n_C_prev = layer['n_C_prev']
            layer['W']=(np.random.rand(f, f, n_C_prev, n_C) - 0.5) * 0.2 # random sample in [-0.1, 0.1] 
            layer['b']=(np.random.rand(1, 1, 1, n_C) - 0.5) * 0.2
            layer['dW']=np.zeros_like(layer['W'])
            layer['db']=np.zeros_like(layer['b'])'''
    
    def forward_prop(self,W1, b1, W2, b2, X):#(784,59000)
    
        X2 = Conv(X,W0)
        Z1 = W1.dot(X) + b1
        A1 = SimpleNN2Layer.ReLU(Z1)
        Z2 = W2.dot(A1) + b2
        A2 = SimpleNN2Layer.softmax(Z2)
        return Z1, A1, Z2, A2    

   
        
    def backward_prop(self,Z1, A1, Z2, A2, W1, W2, X, Y,m):#(784,59000)(59000)    
        one_hot_Y = SimpleNN2Layer.one_hot(Y)
        dZ2 = A2 - one_hot_Y
        dW2 = 1 / m * dZ2.dot(A1.T)
        db2 = 1 / m * np.sum(dZ2)
        dZ1 = W2.T.dot(dZ2) * SimpleNN2Layer.ReLU_deriv(Z1)
        dW1 = 1 / m * dZ1.dot(X.T)
        db1 = 1 / m * np.sum(dZ1)
        return dW1, db1, dW2, db2
    def update_params(self,W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
        W1 = W1 - alpha * dW1
        b1 = b1 - alpha * db1    
        W2 = W2 - alpha * dW2  
        b2 = b2 - alpha * db2    
        return W1, b1, W2, b2
        
        
        
    def get_predictions(self,A2):
        return np.argmax(A2, 0)
    def get_accuracy(self,predictions, Y):
        #print(predictions, Y)
        return np.sum(predictions == Y) / Y.size
    def make_predictions(self,X):
        W1, b1, W2, b2=self.WandB
        _, _, _, A2 = self.forward_prop(W1, b1, W2, b2, X)
        predictions = self.get_predictions(A2)
        return predictions
    
    
    
    def gradient_descent(self,X, Y, alpha, iterations,rows):#self.X_train, self.Y_train, 0.10, 100) 
        W1, b1, W2, b2 = self.WandB
        
        for i in range(iterations):
            
            Z1, A1, Z2, A2 = self.forward_prop(W1, b1, W2, b2, X)
            dW1, db1, dW2, db2 = self.backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y,rows)
            W1, b1, W2, b2 = self.update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
            if i % 10 == 0:
                print("Iteration: ", i)
                predictions = self.get_predictions(A2)
                print(self.get_accuracy(predictions, Y))
        return W1, b1, W2, b2
class SimpleConvLayer():
    def __init__(self):
        self.windows= (platform.system() == "Windows")
        
    def create_logger(self,output_path, cfg_name):
        log_file = '{}_{}.log'.format(cfg_name, time.strftime('%Y-%m-%d-%H-%M'))
        head = '%(asctime)-15s %(message)s'
        filename=os.path.join(output_path, log_file)
        #os.mkdir("output")
        #Utils.savestringfile(filename,"File Create")
        logging.basicConfig(filename=os.path.join(output_path, log_file), format=head)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        return logger

    # Loading and precessing data
    def load_mnist(self,path, kind='train'):
        kind='train'
        """Load MNIST data from `path`"""
        labels_path = os.path.join(path, '%s-labels.idx1-ubyte' % kind)
        images_path = os.path.join(path, '%s-images.idx3-ubyte' % kind)
        with open(labels_path, 'rb') as lbpath:
            magic, n = struct.unpack('>II', lbpath.read(8))
            labels = np.fromfile(lbpath, dtype=np.uint8)

        with open(images_path, 'rb') as imgpath:
            magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
            images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)

        return images, labels

    # %%
    # Parts of Model
    def initialize_parameters(self,layers):
        """
        Initialize parameters according to different types of layers
        
        Argument:
        layers -- list, the length denotes the depth of networks, every element is a dictionary which contains the 
                  mode of layer and shape of weight and bias 
        
        Returns:
        new_layers -- list, every element corresponds to original layer and its intialized parameter
        layer1['mode'] = 'conv'
    layer1['f'] = 5
    layer1['n_C_prev'] = 1
    layer1['n_C'] = 6
    layer1['p'] = 2
    layer1['s'] = 1
        """
        new_layers = []
        for i, layer in enumerate(layers):
            mode = layer['mode'] # 'fc', 'conv', 'pool'
            if mode == 'pool':
                new_layers.append(layer)
                continue
            elif mode == 'fc':
                n_now = layer['n_now']
                n_prev = layer['n_prev']
                layer['W']=(np.random.rand(n_now, n_prev) - 0.5) * 0.2 # random sample in [-0.1, 0.1] 
                layer['b']=(np.random.rand(n_now,1) - 0.5) * 0.2
                layer['dW']=np.zeros_like(layer['W'])
                layer['db']=np.zeros_like(layer['b'])
            elif mode == 'conv':
                f = layer['f']
                n_C = layer['n_C']
                n_C_prev = layer['n_C_prev']
                layer['W']=(np.random.rand(f, f, n_C_prev, n_C) - 0.5) * 0.2 # random sample in [-0.1, 0.1] 
                layer['b']=(np.random.rand(1, 1, 1, n_C) - 0.5) * 0.2
                layer['dW']=np.zeros_like(layer['W'])
                layer['db']=np.zeros_like(layer['b'])
            else:
                print('Wrong layer in [{}]'.format(i))
            new_layers.append(layer)
                
        return new_layers

    def sigmoid(self,Z):
        # Sigmoid activation function
        A = 1/(1+np.exp(-Z))
        cache = Z
        return A, cache

    def sigmoid_backward(self,dA, cache):
        # Backpropogation of sigmoid activation function
        Z = cache
        s = 1/(1+np.exp(-Z))
        dZ = dA * s * (1-s)
        return dZ

    def relu(self,Z):
        # Relu activation function
        A = np.maximum(0,Z)
        cache = Z
        return A, cache

    def relu_backward(self,dA, cache):
        # Backpropogation of Relu activation function 
        Z = cache
        
        dZ = np.array(dA, copy=True) # just converting dz to a correct object.
        dZ[Z < 0] = 0
        return dZ

    def softmax(self,Z):
        # Softmax activation function
        n, m = Z.shape
        A = np.exp(Z)
        A_sum = np.sum(A, axis = 0)
        A_sum = A_sum.reshape(-1, m)
        A = A / A_sum
        cache = Z
        return A, cache

    def softmax_backward(self,A, Y):
        # Backpropogation of softmax activation function
        # loss = - ln a[j] (y[j] = 1, j = {0, ..., n}) 
        m = A.shape[1]
        dZ = (A - Y) / float(m)
        return dZ

    def linear_activation_forward(self,A_prev, layer, activation='relu'):
        W = layer['W']
        b = layer['b']
        if activation=='sigmoid':
            Z, linear_cache=np.dot(W, A_prev)+b, (A_prev, W, b)
            A, activation_cache=self.sigmoid(Z)
        elif activation=='relu':
            Z, linear_cache=np.dot(W, A_prev)+b, (A_prev, W, b)
            A, activation_cache=self.relu(Z)
        else:
            Z = np.dot(W, A_prev)+b
            A = Z
        return A, Z

    def linear_activation_backward(self,dA, layer, activation):
        # Backward propagatIon module - linear activation backward
        A_prev = layer['A_prev']
        W = layer['W']
        b = layer['b']
        Z = layer['Z']
        if activation=='relu':
            dZ=self.relu_backward(dA, Z)
        elif activation=='sigmoid':
            dZ=self.sigmoid_backward(dA, Z)
        else:
            dZ = dA 
        n, m = dA.shape
        dA_prev=np.dot(W.T, dZ)
        dW = np.dot(dZ, A_prev.T)
        db = np.sum(dZ, axis = 1).reshape(n,1)
        
        return dA_prev, dW, db

    def zero_pad(self,X, pad, value = 0):
        """
        Pad with zeros all images of the dataset X. The padding is applied to the height and width of an image, 
        as illustrated in Figure 1.
        
        Argument:
        X -- python numpy array of shape (m, n_H, n_W, n_C) representing a batch of m images
        pad -- integer, amount of padding around each image on vertical and horizontal dimensions
        
        Returns:
        X_pad -- padded image of shape (m, n_H + 2*pad, n_W + 2*pad, n_C)
        """
        X_pad = np.pad(X, ((0, 0),(pad, pad),(pad, pad),(0, 0)), 'constant', constant_values=value)
        
        return X_pad

    def conv_forward(self,A_prev, layer):
        """
        Implements the forward propagation for a convolution function
        
        Arguments:
        A_prev -- output activations of the previous layer, numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
        layer -- a dictionary contains weights, bias, hyperparameters and shape of data
            
        Returns:
        Z -- conv output, numpy array of shape (m, n_H, n_W, n_C)
        """
        # Retrieve information from layer
        W = layer['W']
        b = layer['b']
        stride = layer['s']
        pad = layer['p']
        
        # Retrieve dimensions from A_prev's shape
        (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
        
        # Retrieve dimensions from W's shape
        (f, f, n_C_prev, n_C) = W.shape
        
        # Compute the dimensions of the CONV output volume using the formula given above. Hint: use int() to floor
        n_H = 1 + int((n_H_prev + 2 * pad - f) / stride)
        n_W = 1 + int((n_W_prev + 2 * pad - f) / stride)
        
        # Initialize the output volume Z with zeros
        Z = np.zeros((m, n_H, n_W, n_C))
        
        # Create A_prev_pad by padding A_prev
        if pad > 0:
            A_prev_pad = self.zero_pad(A_prev, pad)
        else:
            A_prev_pad = A_prev
        
        for i in range(m):                                 # loop over the batch of training examples
            a_prev_pad = A_prev_pad[i]                     # Select ith training example's padded activation
            for h in range(n_H):                           # loop over vertical axis of the output volume
                for w in range(n_W):                       # loop over horizontal axis of the output volume
                    for c in range(n_C):                   # loop over channels (= #filters) of the output volume
                        
                        # Find the corners of the current "slice" (≈4 lines)
                        vert_start = h * stride
                        vert_end = vert_start + f
                        horiz_start = w * stride
                        horiz_end = horiz_start + f
                        
                        # Use the corners to define the (3D) slice of a_prev_pad (See Hint above the cell)
                        a_slice_prev = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
                      
                        # Convolve the (3D) slice with the correct filter W and bias b, to get back one output neuron
                        Z[i, h, w, c] = np.sum(np.multiply(a_slice_prev, W[:, :, :, c])) + b[0, 0, 0, c]

        return Z

    def conv_backward(self,dZ, layer):
        """
        Implement the backward propagation for a convolution function
        
        Arguments:
        dZ -- gradient of the cost with respect to the output of the conv layer (Z), numpy array of shape (m, n_H, n_W, n_C)
        layer -- a dictionary contains weights, bias, hyperparameters and shape of data
        
        Returns:
        dA_prev -- gradient of the cost with respect to the input of the conv layer (A_prev),
                   numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
        dW -- gradient of the cost with respect to the weights of the conv layer (W)
              numpy array of shape (f, f, n_C_prev, n_C)
        db -- gradient of the cost with respect to the biases of the conv layer (b)
              numpy array of shape (1, 1, 1, n_C)
        """
        # Retrieve informations from layer
        A_prev = layer['A_prev']
        W = layer['W']
        b = layer['b']
        Z = layer['Z']
        stride = layer['s']
        pad = layer['p']
        
        # Retrieve dimensions from A_prev's shape
        (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
        
        # Retrieve dimensions from W's shape
        (f, f, n_C_prev, n_C) = W.shape
        
        # Retrieve dimensions from dZ's shape
        (m, n_H, n_W, n_C) = dZ.shape
        
        # Initialize dA_prev, dW, db with the correct shapes
        dA_prev = np.zeros((m, n_H_prev, n_W_prev, n_C_prev))                           
        dW = np.zeros((f, f, n_C_prev, n_C))
        db = np.zeros((1, 1, 1, n_C))

        # Pad A_prev and dA_prev
        if pad > 0:
            A_prev_pad = self.zero_pad(A_prev, pad)
            dA_prev_pad = self.zero_pad(dA_prev, pad)
        else:
            A_prev_pad = A_prev
            dA_prev_pad = np.copy(dA_prev)

        for i in range(m):                         # loop over the training examples
            for h in range(n_H):                   # loop over vertical axis of the output volume
                for w in range(n_W):               # loop over horizontal axis of the output volume
                    for c in range(n_C):           # loop over the channels of the output volume
                        
                        # Find the corners of the current "slice"
                        vert_start = h * stride
                        vert_end = vert_start + f
                        horiz_start = w * stride
                        horiz_end = horiz_start + f
                        
                        # Use the corners to define the slice from a_prev_pad
                        a_slice = A_prev_pad[i, vert_start:vert_end, horiz_start:horiz_end, :]

                        # Update gradients for the window and the filter's parameters using the code formulas
                        dA_prev_pad[i, vert_start:vert_end, horiz_start:horiz_end, :] += W[:,:,:,c] * dZ[i, h, w, c]
                        dW[:,:,:,c] += dZ[i, h, w, c] * a_slice
                        db[:,:,:,c] += dZ[i, h, w, c]
                        
                        
            # Set the ith training example's dA_prev to the unpaded da_prev_pad
            if pad == 0:
                dA_prev[i, :, :, :] = dA_prev_pad[i, :, :, :]
            else:
                dA_prev[i, :, :, :] = dA_prev_pad[i, pad:-pad, pad:-pad, :]
        
        return dA_prev, dW, db

    def pool_forward(self,A_prev, layer, mode = "max"):
        """
        Implements the forward pass of the pooling layer
        
        Arguments:
        A_prev -- Input data, numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
        hparameters -- python dictionary containing "f" and "stride"
        mode -- the pooling mode you would like to use, defined as a string ("max" or "average")
        
        Returns:
        A -- output of the pool layer, a numpy array of shape (m, n_H, n_W, n_C)
        """
        # Retrieve dimensions from the input shape
        (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
        
        # Retrieve hyperparameters from "hparameters"
        f = layer["f"]
        stride = layer["s"]
        
        # Define the dimensions of the output
        n_H = int(1 + (n_H_prev - f) / stride)
        n_W = int(1 + (n_W_prev - f) / stride)
        n_C = n_C_prev
        
        # Initialize output matrix A
        A = np.zeros((m, n_H, n_W, n_C))              

        for i in range(m):                           # loop over the training examples
            for h in range(n_H):                     # loop on the vertical axis of the output volume
                for w in range(n_W):                 # loop on the horizontal axis of the output volume
                    for c in range (n_C):            # loop over the channels of the output volume
                        
                        # Find the corners of the current "slice"
                        vert_start = h * stride
                        vert_end = vert_start + f
                        horiz_start = w * stride
                        horiz_end = horiz_start + f
                        
                        # Use the corners to define the current slice on the ith training example of A_prev, channel c.
                        a_prev_slice = A_prev[i, vert_start:vert_end, horiz_start:horiz_end, c]
                        
                        # Compute the pooling operation on the slice. Use an if statment to differentiate the modes.
                        if mode == "max":
                            A[i, h, w, c] = np.max(a_prev_slice)
                        elif mode == "average":
                            A[i, h, w, c] = np.mean(a_prev_slice)

        return A

    def distribute_value(self,dz, shape):
        """
        Distributes the input value in the matrix of dimension shape
        
        Arguments:
        dz -- input scalar
        shape -- the shape (n_H, n_W) of the output matrix for which we want to distribute the value of dz
        
        Returns:
        a -- Array of size (n_H, n_W) for which we distributed the value of dz
        """
        # Retrieve dimensions from shape
        (n_H, n_W) = shape
        # Compute the value to distribute on the matrix
        average = dz / (n_H * n_W)
        # Create a matrix where every entry is the "average" value
        a = np.ones(shape) * average
        
        return a

    def create_mask_from_window(self,x):
        """
        Creates a mask from an input matrix x, to identify the max entry of x.
        Arguments:
        x -- Array of shape (f, f)
        Returns:
        mask -- Array of the same shape as window, contains a True at the position corresponding to the max entry of x.
        """
        mask = (x == np.max(x))
        
        return mask

    def pool_backward(self,dA, layer, mode = "max"):
        """
        Implements the backward pass of the pooling layer
        
        Arguments:
        dA -- gradient of cost with respect to the output of the pooling layer, same shape as A
        cache -- cache output from the forward pass of the pooling layer, contains the layer's input and hparameters 
        mode -- the pooling mode you would like to use, defined as a string ("max" or "average")
        
        Returns:
        dA_prev -- gradient of cost with respect to the input of the pooling layer, same shape as A_prev
        """
        # Retrieve information from layer
        A_prev = layer['A_prev']
        stride = layer['s']
        f = layer['f']
        
        # Retrieve dimensions from A_prev's shape and dA's shape
        m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape
        m, n_H, n_W, n_C = dA.shape
        
        # Initialize dA_prev with zeros
        dA_prev = np.zeros_like(A_prev)
        
        for i in range(m):                         # loop over the training examples
            # select training example from A_prev
            a_prev = A_prev[i]
            for h in range(n_H):                   # loop on the vertical axis
                for w in range(n_W):               # loop on the horizontal axis
                    for c in range(n_C):           # loop over the channels (depth)
                        # Find the corners of the current "slice" 
                        vert_start = h * stride
                        vert_end = vert_start + f
                        horiz_start = w * stride
                        horiz_end = horiz_start + f
                        
                        # Compute the backward propagation in both modes.
                        if mode == "max":
                            # Use the corners and "c" to define the current slice from a_prev
                            a_prev_slice = a_prev[vert_start:vert_end, horiz_start:horiz_end, c]
                            # Create the mask from a_prev_slice
                            mask = self.create_mask_from_window(a_prev_slice)
                            # Set dA_prev to be dA_prev + (the mask multiplied by the correct entry of dA)
                            dA_prev[i, vert_start: vert_end, horiz_start: horiz_end, c] += mask * dA[i, h, w, c]
                            
                        elif mode == "average":
                            # Get the value a from dA
                            da = dA[i, h, w, c]
                            # Define the shape of the filter as fxf
                            shape = (f, f)
                            # Distribute it to get the correct slice of dA_prev. i.e. Add the distributed value of da.
                            dA_prev[i, vert_start: vert_end, horiz_start: horiz_end, c] += self.distribute_value(da, shape)

        return dA_prev

    def forward_propogation(self,X, layers):
        m = X.shape[0]
        # -1- convolution layer
        layers[0]['A_prev'] = X
        Z = self.conv_forward(X, layers[0])
        layers[0]['Z'] = Z
        A, _ = self.relu(Z)
        
        # -2- average pooling layer
        layers[1]['A_prev'] = A
        A = self.pool_forward(A, layers[1], mode = "average")
        
        # -3- convolution layer
        layers[2]['A_prev'] = A
        Z = self.conv_forward(A, layers[2])
        layers[2]['Z'] = Z
        A, _ = self.relu(Z)
        
        # -4- average pooling layer
        layers[3]['A_prev'] = A
        A = self.pool_forward(A, layers[3], mode = "average")
        
        # -5- convolution layer
        layers[4]['A_prev'] = A
        Z = self.conv_forward(A, layers[4])
        layers[4]['Z'] = Z
        A, _ = self.relu(Z)
        
        # -6- fully connected layer
        layers[5]['A_prev'] = (A.reshape(m,-1)).T # flatten
        A, Z = self.linear_activation_forward((A.reshape(m,-1)).T, layers[5], activation='relu')
        layers[5]['Z'] = Z
        
        # -7- fully connected layer
        layers[6]['A_prev'] = A
        _, Z = self.linear_activation_forward(A, layers[6], activation='none')
        layers[6]['Z'] = Z
        AL, _ = self.softmax(Z)

        return AL, layers

    def compute_cost(self,AL, Y):
        n, m = Y.shape
        cost = - np.sum(np.log(AL) * Y) / m
        cost=np.squeeze(cost)

        return cost

    def backward_propogation(self,AL, Y, layers):
        m = Y.shape[1]
        # -7- fully connected layer
        dZ = self.softmax_backward(AL, Y)
        dA_prev, dW, db = self.linear_activation_backward(dZ, layers[6], 'none')
        layers[6]['dW'] = dW
        layers[6]['db'] = db
        
        # -6- fully connected layer
        dA_prev, dW, db = self.linear_activation_backward(dA_prev, layers[5], 'relu')
        layers[5]['dW'] = dW
        layers[5]['db'] = db
        
        # -5- convolution layer
        dA = (dA_prev.T).reshape(m,1,1,layers[4]['n_C']) # flatten backward
        dZ = self.relu_backward(dA, layers[4]['Z'])
        dA_prev, dW, db = self.conv_backward(dZ, layers[4])
        layers[4]['dW'] = dW
        layers[4]['db'] = db
        
        # -4- average pooling layer
        dA_prev = self.pool_backward(dA_prev, layers[3], mode = "average")
        
        # -3- convolution layer
        dZ = self.relu_backward(dA_prev, layers[2]['Z'])
        dA_prev, dW, db = self.conv_backward(dZ, layers[2])
        layers[2]['dW'] = dW
        layers[2]['db'] = db
        
        # -2- average pooling layer
        dA_prev = self.pool_backward(dA_prev, layers[1], mode = "average")
        
        # -1- convolution layer
        dZ = self.relu_backward(dA_prev, layers[0]['Z'])
        dA_prev, dW, db = self.conv_backward(dZ, layers[0])
        layers[0]['dW'] = dW
        layers[0]['db'] = db
        
        return layers

    def update_parameters(self,layers, learning_rate):
        num_layer = len(layers)
        for i in range(num_layer):
            mode = layers[i]['mode'] # 'fc', 'conv', 'pool'
            if mode == 'pool':
                continue
            elif (mode == 'fc' or mode == 'conv'):
                layers[i]['W'] = layers[i]['W'] - learning_rate*layers[i]['dW']
                layers[i]['b'] = layers[i]['b'] - learning_rate*layers[i]['db']
            else:
                print('Wrong layer mode in [{}]'.format(i))

        return layers

    def predict(self,X_test, Y_test, layers):
        m = X_test.shape[0]
        n = Y_test.shape[1]
        pred = np.zeros((n,m))
        pred_count = np.zeros((n,m)) - 1 # for counting accurate predictions 
        
        # Forward propagation
        AL, _ = self.forward_propogation(X_test, layers)

        # convert prediction to 0/1 form
        max_index = np.argmax(AL, axis = 0)
        pred[max_index, list(range(m))] = 1
        pred_count[max_index, list(range(m))] = 1
        
        accuracy = float(np.sum(pred_count == Y_test.T)) / m
        
        return pred, accuracy

    def compute_accuracy(self,AL, Y):
        n, m = Y.shape
        pred_count = np.zeros((n,m)) - 1
        
        max_index = np.argmax(AL, axis = 0)
        pred_count[max_index, list(range(m))] = 1
        
        accuracy = float(np.sum(pred_count == Y)) / m
        
        return accuracy

    def train_mini_batch(self,X_train, Y_train, X_test, Y_test, layers, logger, num_exp=0, batch_size=10, num_epoch=1, learning_rate=0.01):
        logger.info('------------ Integer order CNN with mini batch ------------')
        logger.info('Initial weights: FC [-0.1, 0.1], CONV [-0.1, 0.1]')
        logger.info('Initial bias: FC [-0.1, 0.1], CONV [-0.1, 0.1]')
        logger.info('Batch size: {}'.format(batch_size))
        logger.info('Learning rate: {}'.format(learning_rate))
        
        # number of iteration
        num_sample=X_train.shape[0]
        num_iteration = num_sample // batch_size
        index = list(range(num_sample))
        print(num_sample,num_iteration)
        accuracy_train_list = []
        accuracy_test_list = []
        for epoch in range(num_epoch):
            losses = []
            accuracies = []
            random.seed(num_exp*10+epoch)
            random.shuffle(index) # random sampling every epoch
            for iteration in range(num_iteration):
                batch_start = iteration * batch_size
                batch_end = (iteration + 1) * batch_size
                if batch_end > num_sample:
                    batch_end = num_sample
                X_train_batch = X_train[index[batch_start:batch_end]]
                Y_train_batch = Y_train[index[batch_start:batch_end]]
                ck=clock()
                AL, layers = self.forward_propogation(X_train_batch, layers)#bsize=10
                print("\r\n\size",len(X_train_batch),batch_size,clock()-ck)
                loss = self.compute_cost(AL, Y_train_batch.T)
                accuracy = self.compute_accuracy(AL, Y_train_batch.T)
                layers = self.backward_propogation(AL, Y_train_batch.T, layers)
                layers = self.update_parameters(layers, learning_rate)
                losses.append(loss)
                accuracies.append(accuracy)
                if (iteration+1) % 600 == 0:
                    logger.info('Epoch [{}] Iteration [{}]: loss = {} accuracy = {}'.format(epoch, iteration+1, loss, accuracy))
                    print('Epoch [{}] Iteration [{}]: loss = {} accuracy = {}'.format(epoch, iteration+1, loss, accuracy))
                    np.save('data/layers_{}_{}.npy'.format(epoch, iteration+1), layers)

            _, accuracy_test = self.predict(X_test, Y_test, layers)
            pred_train, _ = self.forward_propogation(X_train[:10000], layers)
            loss_train = self.compute_cost(pred_train, Y_train[:10000].T)
            accuracy_train = self.compute_accuracy(pred_train, Y_train[:10000].T)
            accuracy_train_list.append(accuracy_train)
            accuracy_test_list.append(accuracy_test)
            print('Epoch [{}] average_loss = {} average_accuracy = {}'.format(epoch, np.mean(losses), np.mean(accuracies)))
            logger.info('Epoch [{}] average_loss = {} average_accuracy = {}'.format(epoch, np.mean(losses), np.mean(accuracies)))
            print('Epoch [{}] train_loss = {} train_accuracy = {}'.format(epoch, loss_train, accuracy_train))
            logger.info('Epoch [{}] train_loss = {} train_accuracy = {}'.format(epoch, loss_train, accuracy_train))
            print('Epoch [{}] test_accuracy = {}'.format(epoch, accuracy_test))
            logger.info('Epoch [{}] test_accuracy = {}'.format(epoch, accuracy_test))
        
        return layers, accuracy_train_list, accuracy_test_list

    def LoadModel(self):
        # %%
        # Create log file
        logger = self.create_logger('output', 'train_log')

        # Load dataset and reshape image set as (m, n_H, n_W, n_C)
        X_train, Y_train = self.load_mnist('data', 'train')
        X_test, Y_test = self.load_mnist('data', 'test')
        X_train = X_train.reshape(-1,28,28,1)
        X_test = X_test.reshape(-1,28,28,1)

        # Normalization for images
        X_train = X_train / 255.0
        X_test = X_test / 255.0

        # Transform the label into one-hot form
        (num_train,) = Y_train.shape
        Y = np.zeros((num_train, 10))
        for i in range(num_train):
            Y[i, Y_train[i]] = 1
        Y_train = Y
        (num_test,) = Y_test.shape
        Y = np.zeros((num_test, 10))
        for i in range(num_test):
            Y[i, Y_test[i]] = 1
        Y_test = Y

        # Construct model
        layer1={}
        layer1['mode'] = 'conv'
        layer1['f'] = 5
        layer1['n_C_prev'] = 1
        layer1['n_C'] = 6
        layer1['p'] = 2
        layer1['s'] = 1
        layer2={}
        layer2['mode'] = 'pool'
        layer2['f'] = 2
        layer2['s'] = 2
        layer3={}
        layer3['mode'] = 'conv'
        layer3['f'] = 5
        layer3['n_C_prev'] = 6
        layer3['n_C'] = 16
        layer3['p'] = 0
        layer3['s'] = 1
        layer4={}
        layer4['mode'] = 'pool'
        layer4['f'] = 2
        layer4['s'] = 2
        layer5={}
        layer5['mode'] = 'conv'
        layer5['f'] = 5
        layer5['n_C_prev'] = 16
        layer5['n_C'] = 120
        layer5['p'] = 0
        layer5['s'] = 1
        layer6={}
        layer6['mode'] = 'fc'
        layer6['n_now'] = 84
        layer6['n_prev'] = 120
        layer7={}
        layer7['mode'] = 'fc'
        layer7['n_now'] = 10
        layer7['n_prev'] = 84
        construct_layers = [layer1, layer2, layer3, layer4, layer5, layer6, layer7]

        # %%
        num_experiments = 1
        for index in range(num_experiments):
            print('------------------------------------- Experiment {} -------------------------------------'.format(index+1))
            logger.info('------------------------------------- Experiment {} -------------------------------------'.format(index+1))

            initial_layers_path = 'data/initial_layers_{}.npy'.format(index+1)
            if os.path.exists(initial_layers_path):
                print(initial_layers_path)
                initial_layers = np.load(initial_layers_path, allow_pickle=True)
                print('Load initial parameters from {}'.format(initial_layers_path))
                logger.info('Load initial parameters from {}'.format(initial_layers_path))
            else:
                initial_layers = self.initialize_parameters(construct_layers)
                np.save(initial_layers_path, initial_layers)
                print('Initialize layers and save as {}'.format(initial_layers_path))
                logger.info('Initialize layers and save as {}'.format(initial_layers_path))
            
            print('----------------------------------------------------------------------------------------')
            logger.info('----------------------------------------------------------------------------------------')
            layers, train_acc, test_acc = self.train_mini_batch(X_train, Y_train, X_test, Y_test, initial_layers,
                                            logger, num_exp=index, batch_size=10, num_epoch=1, learning_rate=0.1)
            print('\n')
            logger.info('\n')
    
