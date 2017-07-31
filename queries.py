# -*- coding: utf-8 -*-
# Author: Dante Fernando Bazaldua Huerta

import pyrebase
from prettytable import PrettyTable
class Queries( object ):

    firebase    = None
    user        = None
    # Local variables
    auth_local  = None
    db          = None
    storage     = None

    information = None
    id_tr       = None


    def __init__( self, confobj = None, usrobj = None ):
        try:
            self.firebase    = pyrebase.initialize_app( confobj )
            self.auth_local  = self.firebase.auth() # En caso de necesitar insertar información

            self.user = self.auth_local.sign_in_with_email_and_password(usrobj['user'],usrobj['pass'])
            self.setLocalVariables() # Crear las variables locales necesarias para hacer request a la base de datos.

        except Exception as e:
            print e

    def setLocalVariables( self ):
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

    def getValue( self, criterio, id ):
        try:
            value = self.db.child(criterio).child( id ).get()
            if value is not None:
                return value.val(), value.key()
            return None
        except Exception as e:
            print e
            return None

    def reprocess( self ):
        try:
            print "Reprocesar: %s" %( self.id_tr )
            self.db.child("Transfer").child(self.id_tr).update({"processed": False})
            print "Completado! Bye :)"

        except Exception as e:
            print e


    def thirdEye( self, rawData, idtransfer ):
        """
        thirdEye is a function which create all the queries and show the information in the screen.
        Params:
        rawData - The information of the transaction
        idtransfer - The transaction key
        """
        # Se guarda como atributo de la clase
        self.information = rawData
        self.id_tr  = idtransfer

        idp = rawData[ idtransfer ]['key_persona']
        ide = rawData[ idtransfer ]['key_empresa']
        idv = rawData[ idtransfer ]['key_encuesta']

        persona, pkey = self.getValue( 'Personas', idp )
        empresa, ekey = self.getValue( 'Cuenta', ide )
        encuesta, vkey = self.getValue( 'Encuestas', idv )

        resume = PrettyTable()
        resume.field_names = ["Campo","Valor","Id"]

        if empresa != None and persona != None and encuesta != None:
            print "\nResumen: ( %s )" %( str(idtransfer))
            resume.add_row(['Fecha',rawData[ idtransfer ]['date'],'-'])
            if 'date_final' in rawData[ idtransfer ]:
                fecha = rawData[ idtransfer ]['date_final']
            else:
                fecha = "Sin informacion"
            resume.add_row(['Fecha CLOUD', fecha,'-'])
            resume.add_row(['Nombre',persona['Nombre'] + " " + persona['ApPat'] + " " + persona['ApMat'], pkey])
            resume.add_row(['Evaluacion', encuesta['clasificacion'], vkey])
            resume.add_row(['Empresa', empresa['NComercial'], ekey])
            resume.add_row(['Procesado', rawData[ idtransfer ][ 'processed' ], '-'])

            print resume

            print "Resultado(Evaluacion): \n%s" %( rawData[ idtransfer ]['resultado'])

        else:

            print "No hay suficientes datos para mostrar el resultado."

    def requestByUserId( self, id ):
        """
        This method is used to get the information of any transaction with a match of the person key.
        Params:
        id - Person Key
        """
        try:

            whois = self.db.child("Transfer").order_by_child("key_persona").equal_to( str(id) ).get()
            # Aquí lo da con todo y ID
            if whois is not None:
                raw = whois.val()
                for e in raw:
                    key = e
                    break

                self.thirdEye( raw, key )

        except Exception as e:
            print e

    def requestByTransferId( self, id ):
        """
        This method allows to check which info is in the transfer branch.
        Params:
        id - Transfer Key
        """
        try:

            raw = {}
            whois = self.db.child('Transfer/'+id).get()

            if whois is not None:
                key = whois.key()
                raw[ whois.key() ] = whois.val()
                self.thirdEye( raw, key )

        except Exception as e:
            print e

    def getUsersById( self, id ):
        """
//TODO: USER description
        """
        try:

            whois = self.db.child("Usuarios").order_by_child("Empresa").equal_to( str(id) ).get()
            # Aquí lo da con todo y ID
            if whois is not None:
                raw = whois.val()
                print "Existen: %d" % ( len( raw ) )
                count = 1
                for e in raw:
                    print "%d - %s" % ( count, raw[ e ][ 'email' ] )
                    count = count + 1

        except Exception as e:
            print e
