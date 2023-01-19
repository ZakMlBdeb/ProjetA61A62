import os
import uuid
import flask
import urllib
from PIL import Image
from tensorflow import keras
from keras.models import load_model
from flask import Flask , render_template  , request , send_file
from keras.utils import load_img , img_to_array

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = keras.models.load_model(os.path.join(BASE_DIR , 'model_alzheimer01.h5'))


EXTENSIONS_AUTORISEES = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def fichier_autorise(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in EXTENSIONS_AUTORISEES

classes = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']


def predire(filename , model):
    img = load_img(filename , target_size = (128,128))
    img = img_to_array(img)
    img = img.reshape(1 , 128,128,3)

    img = img.astype('float32')
    result = model.predict(img)

    dict_result = {}
    for i in range(4):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:4]

    prob_result = []
    class_result = []
    for i in range(4):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result , prob_result




@app.route('/')
def home():
        return render_template("index.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result , prob_result = predire(img_path , model)

                predictions = {
                        "class1":class_result[0],
                        "class2":class_result[1],
                        "class3":class_result[2],
                        "class4":class_result[3],
                        "prob1": prob_result[0],
                        "prob2": prob_result[1],
                        "prob3": prob_result[2],
                        "prob4": prob_result[3],
                }

            except Exception as e :
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('index.html' , error = error)


        elif (request.files):
            file = request.files['file']
            if file and fichier_autorise(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                class_result , prob_result = predire(img_path , model)

                predictions = {
                        "class1":class_result[0],
                        "class2":class_result[1],
                        "class3":class_result[2],
                        "class4":class_result[3],
                        "prob1": prob_result[0],
                        "prob2": prob_result[1],
                        "prob3": prob_result[2],
                        "prob4": prob_result[3],
                }

            else:
                error = "Veuillez Charger une image avec jpg , jpeg et/ou png extension seulement"

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('index.html' , error = error)

    else:
        return render_template('index.html')

 # return {
 #        "class": predicted_class,
 #        "confidence": float(confidence)
 #    }

if __name__ == "__main__":
    app.run(debug = True)



