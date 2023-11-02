import discord
import csv
import os
intents = discord.Intents.all()
client = discord.Client(intents=intents)

directory = "nameOfDirectory"
filename = 'coordinates.csv'

         

class AMDCsv(object):
    __instance = None

    def __new__(cls):
        if AMDCsv.__instance is None:
            AMDCsv.__instance = object.__new__(cls)
        return AMDCsv.__instance

    def createCSV(self):
    
        pathFile = directory+filename
        if not os.path.exists(pathFile):
            with open(directory+filename, mode='w', newline='') as archivo_csv:
                csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            archivoCreado = True
            print("Creado")
        else:
            print("Archivo ya creado")

        
        

    def checkCoordinates(self,server,game,target):
        with open(directory+filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)
            left, right = 0, len(lines) - 1
            
        while left <= right:
            mid = (left + right) // 2
            if lines[mid][0] == target:
                return lines[mid]
            elif lines[mid][0] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return None
    
    def insertCoordinates(self,server,game,place,coordinatesx,coordinatesy,coordinatez):
        row = [server,game,place,coordinatesx,coordinatesy,coordinatez]
        with open(directory+filename, mode='a', newline='') as csvfile:
            coordinatesWriter = csv.writer(csvfile)
            coordinatesWriter.writerow(row)
    
    def deleteCoordinates(self,server,game,coordinates):
        return True


class coordenadasMinecraft:
    def __init__(self,nombreLugar,CoordenadasX,CoordenadasY, CoordenadasZ):
       
        self.nombreLugar = nombreLugar
        self.CoordenadasX = CoordenadasX
        self.CoordenadasY = CoordenadasY
        self.CoordenadasZ = CoordenadasZ
    
    def __repr__(self):
        return 'El nombre del lugar es {0}: {1} {2} {3}\n'.format(self.nombreLugar,self.CoordenadasX ,self.CoordenadasY, self.CoordenadasZ)

class MyClient(discord.Client):
    global csvGenerator
    csvGenerator = AMDCsv()
    csvGenerator.createCSV()


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
    
    async def on_message(self,message):
       

        if message.content.startswith('!formatoCoordenadas'):
            await message.reply(formatoCoordenadas(message),mention_author=True)

        if message.content.startswith('!coordenadas'):
            
            await message.reply(AMDCoordenadas(message),mention_author=True)

        if message.content.startswith('!verCoordenadas'):
            await message.reply(verCoordenadas(message),mention_author = True)

        if message.content.startswith('!borrarCoordenadas'):
            await message.reply(deleteCoordinates(message),mention_author = True) 



        if message.content.startswith('!nameServer'):           

             
            await message.reply(nameServer(message),mention_author=True)       


def ACoordinatesMinecraft(message):
    
    serverName = message.guild.name
    messageAux =  message.content.split(' ')
    csvGenerator.insertCoordinates(serverName,messageAux[1],messageAux[2],messageAux[3],messageAux[4],messageAux[5])

 


def AMDCoordenadas(message):


    messageAux = message.content.split(' ') 
    if(messageAux[1]) == 'Minecraft' or messageAux[1] == 'minecraft':
        
        ACoordinatesMinecraft(message)



    return 'Las coordenadas fueron agregadas con exito'



def verCoordenadas(message):
    coordinatesGame = [] 
    with open(directory+filename, 'r', newline='') as archive:
        lector = csv.reader(archive)
        coordinates = archive.readlines()
        for coordinate in coordinates:
            infoCoordinate = coordinate.split(',')
            if infoCoordinate[0] == message.guild.name:
                minecraftCoordinate = coordenadasMinecraft(infoCoordinate[2],infoCoordinate[3],infoCoordinate[4],infoCoordinate[5])
                coordinatesGame.append(minecraftCoordinate)
    
    return (' '.join(map(str,coordinatesGame)))


def formatoCoordenadas(message):
    return 'Para agregar coordenadas, debe seguir este formato, donde el nombre del lugar no tenga espacios: !coordenadas Minecraft nombreLugar CoordenadaX CoordenadaY CoordenadZ'


def deleteCoordinates(message):
    csvGenerator.deleteCoordinatesin
    return False

def nameServer(message):
    return message.guild.name




client = MyClient(intents=intents)
client.run('tokenBot')
