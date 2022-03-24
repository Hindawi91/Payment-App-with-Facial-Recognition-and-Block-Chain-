import face_recognition
import cv2
import numpy as np
import os
import glob
import time


def get_facename():
    faces_encodings = []
    faces_names = []
    
    data_path = './data/'
    face_encodings_folder = './faces_encodings/'
    face_encodings_path = './faces_encodings/faces_encodings.npy'
    
    if not os.path.exists(face_encodings_path):
        if not os.path.exists(face_encodings_folder):
            os.makedirs(face_encodings_folder)
            
        for file in os.listdir(data_path):
            
            name = file.replace(".jpg", "")
            
            img_path = f"{data_path}{file}"
            
            img = face_recognition.load_image_file(img_path)
            
            face_encoding = face_recognition.face_encodings(img)[0]
            
            faces_names.append(name)
            faces_encodings.append(face_encoding)
            
        faces_encodings = np.asarray(faces_encodings)
        
        np.save('./faces_encodings/faces_names', faces_names)
        np.save('./faces_encodings/faces_encodings', faces_encodings)
    
    else:
        faces_encodings = np.load('./faces_encodings/faces_encodings.npy')
        faces_names = np.load('./faces_encodings/faces_names.npy')
    
    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    
    cv2.destroyAllWindows() 
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while True:
        
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
    
            
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
            face_names = []
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces (faces_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    # print(best_match_index)
                    
                    counter = 0 
                    
                    last_saved_index = best_match_index
                    while counter<3:
                        
                        if best_match_index == last_saved_index:
                            counter +=1
                        else:
                            counter = 0
                    # print("loop broken")
                    
                    name = faces_names[best_match_index]
                face_names.append(name)
                
        process_this_frame = not process_this_frame
    # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    
    # make sure we get consistent readings

        if len(face_names) > 0 :
            if face_names[0] in faces_names:
                # print (face_names[0])
                
                cv2.putText(frame, "Name captured", (face_locations[0][3] + 6, face_locations[0][1] - 6), font, 1.0, (255, 255, 255), 1)
                cv2.imshow('Video', frame)
                cv2.waitKey(3000)
                
                # time.sleep(3)
                break
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    video_capture.release()
    cv2.destroyAllWindows()    
    return face_names[0]

if __name__ == "__main__":
   get_facename()