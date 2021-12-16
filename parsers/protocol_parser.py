class ProtocolParser:

    def insertByteNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertByte(fieldName, payload, index - 2, use_G_field)

    def insertByte(self, fieldName, payload, index, use_G_field):
        value = self.indexToByte(index + 2, 1, payload)
        if use_G_field:
            self.G_fields[fieldName] = value
        else:
            self.H_fields[fieldName] = value
        return index + 4

    def insertByteListNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertByteList(fieldName, payload, index - 2, use_G_field)

    def insertByteList(self, fieldName, payload, index, use_G_field):
        value = self.indexToByte(index + 2, 1, payload)
        if use_G_field:
            if fieldName not in self.G_fields.keys():
                self.G_fields[fieldName] = [value]
            elif value not in self.G_fields[fieldName]:
                self.G_fields[fieldName].append(value)
        else:
            if fieldName not in self.H_fields.keys():
                self.H_fields[fieldName] = [value]
            elif value not in self.H_fields[fieldName]:
                self.H_fields[fieldName].append(value)
        return index + 4


    def insertTwoBytesNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertTwoBytes(fieldName, payload, index - 2, use_G_field)

    def insertTwoBytes(self, fieldName, payload, index, use_G_field):
        value = self.indexToByte(index + 2, 2, payload)
        if use_G_field:
            self.G_fields[fieldName] = value
        else:
            self.H_fields[fieldName] = value
        return index + 6

    def insertFourBytesNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertFourBytes(fieldName, payload, index - 2, use_G_field)

    def insertFourBytes(self, fieldName, payload, index, use_G_field):
        value = self.indexToByte(index + 2, 4, payload)
        if use_G_field:
            self.G_fields[fieldName] = value
        else:
            self.H_fields[fieldName] = value
        return index + 10

    def insertStringNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertString(fieldName, payload, index - 2, use_G_field)

    def insertString(self, fieldName, payload, index, use_G_field):
        stringLength = int(self.indexToByte(index+2, 2, payload), 16)
        value = self.indexToByte(index + 6, stringLength, payload)
        if use_G_field:
            self.G_fields[fieldName] = value
        else:
            self.H_fields[fieldName] = value
        return index + 6 + (stringLength * 2)

    def insertStringListNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertStringList(fieldName, payload, index - 2, use_G_field)

    def insertStringList(self, fieldName, payload, index, use_G_field):
        stringLength = int(self.indexToByte(index+2, 2, payload), 16)
        value = self.indexToByte(index + 6, stringLength, payload)
        if use_G_field:
            if fieldName not in self.G_fields.keys():
                self.G_fields[fieldName] = [value]
            elif value not in self.G_fields[fieldName]:
                self.G_fields[fieldName].append(value)
        else:
            if fieldName not in self.H_fields.keys():
                self.H_fields[fieldName] = [value]
            elif value not in self.H_fields[fieldName]:
                self.H_fields[fieldName].append(value)
        return index + 6 + (stringLength * 2)

    def insertStringPair(self, fieldName, payload, index, key_Use_G_field, value_Use_G_field):
        index = self.insertString(fieldName + " key", payload, index, key_Use_G_field)
        index = self.insertString(fieldName + " value", payload, index - 2, value_Use_G_field)
        return index

    def insertVariableByteIntegerNoIdentifier(self, fieldName, payload, index, use_G_field):
        return self.insertVariableByteInteger(fieldName, payload, index - 2, use_G_field)

    # Simply conver the remaining length field into an integer
    def remainingLengthToInteger(self):
        multiplier = 1
        sum = 0
        for i in range(0, len(self.remaining_length), 2):
            sum += int(self.remaining_length[i:i+2], 16) * multiplier
            multiplier *= 128
        return sum

    def insertVariableByteInteger(self, fieldName, payload, index, use_G_field):
        index += 2
        startIndex = index
        multiplier = 1
        while True:
            encodedByte = int(self.indexToByte(index, 1, payload), 16)
            index += 2
            multiplier *= 128
            if encodedByte & 128 == 0:
                break

        value = payload[startIndex:index]
        if use_G_field:
            self.G_fields[fieldName] = value
        else:
            self.H_fields[fieldName] = value
        
        return index

    # This is really just the same as insertString(), but the resulting
    # data is not restricted to ASCII characters. Not relevant for parsing.
    def insertBinaryData(self, fieldName, payload, index, use_G_field):
        return self.insertString(fieldName, payload, index, use_G_field)

    # Called from parseProperties(). This function does the 
    # actual parsing.
    def parsePropertiesHelper(self, properties):
        index = 0
        while index < len(properties):
            if self.indexToByte(index, 1, properties) == '01':
                index = self.insertByte("payload format indicator", properties, index, True)
            
            if self.indexToByte(index, 1, properties) == '02':
                index = self.insertFourBytes("message expiry interval", properties, index, False)

            if self.indexToByte(index, 1, properties) == '03':
                index = self.insertString("content type", properties, index, False)

            if self.indexToByte(index, 1, properties) == '08':
                index = self.insertString("response topic", properties, index, False)

            if self.indexToByte(index, 1, properties) == '09':
                index = self.insertBinaryData("correlation data", properties, index, False)

            if self.indexToByte(index, 1, properties) == '0b':
                index = self.insertVariableByteInteger("subscription identifier", properties, index, False)
            
            if self.indexToByte(index, 1, properties) == '11':
                index = self.insertFourBytes("session expiry interval", properties, index, False)

            if self.indexToByte(index, 1, properties) == '12':
                index = self.insertString("assigned client identifier", properties, index, False)
            
            if self.indexToByte(index, 1, properties) == '13':
                index = self.insertTwoBytes("server keep alive", properties, index, False)
            
            if self.indexToByte(index, 1, properties) == '15':
                index = self.insertString("authentication method", properties, index, False)

            if self.indexToByte(index, 1, properties) == '16':
                index = self.insertBinaryData("authentication data", properties, index, False)

            if self.indexToByte(index, 1, properties) == '17':
                index = self.insertByte("request problem information", properties, index, True)

            if self.indexToByte(index, 1, properties) == '18':
                index = self.insertFourBytes("will delay interval", properties, index, False)

            if self.indexToByte(index, 1, properties) == '19':
                index = self.insertByte("request response information", properties, index, True)

            if self.indexToByte(index, 1, properties) == '1a':
                index = self.insertString("response information", properties, index, True)

            if self.indexToByte(index, 1, properties) == '1c':
                index = self.insertString("server reference", properties, index, True)

            if self.indexToByte(index, 1, properties) == '1f':
                index = self.insertString("reason string", properties, index, False)
            
            if self.indexToByte(index, 1, properties) == '21':
                index = self.insertTwoBytes("receive maximum", properties, index, True)

            if self.indexToByte(index, 1, properties) == '22':
                index = self.insertTwoBytes("topic alias maximum", properties, index, True)

            if self.indexToByte(index, 1, properties) == '23':
                index = self.insertTwoBytes("topic alias", properties, index, False)

            if self.indexToByte(index, 1, properties) == '24':
                index = self.insertByte("maximum qos", properties, index, True)

            if self.indexToByte(index, 1, properties) == '25':
                index = self.insertByte("retain available", properties, index, True)

            if self.indexToByte(index, 1, properties) == '26':
                index = self.insertStringPair("user property", properties, index, False, False)

            if self.indexToByte(index, 1, properties) == '27':
                index = self.insertFourBytes("maximum packet size", properties, index, True)

            if self.indexToByte(index, 1, properties) == '28':
                index = self.insertByte("wildcard subscription available", properties, index, True)

            if self.indexToByte(index, 1, properties) == "29":
                index = self.insertByte("subscription identifier available", properties, index, True)

            if self.indexToByte(index, 1, properties) == "2a":
                index = self.insertByte("shared subscription available", properties, index, True)
        

    # Parse the Properties header in the payload.
    # It is assumed that index points to the Property Length field.
    # This function just finds the properties substring within the payload
    # and passes that to parsePropertiesHelper().
    def parseProperties(self):
        if len(self.payload[self.index:]) == 0:
            return
        multiplier = 1
        propertyLength = 0
        while True:
            encodedByte = int(self.indexToByte(self.index), 16)
            self.index += 2
            propertyLength += (encodedByte & 127) * multiplier
            multiplier *= 128
            if encodedByte & 128 == 0:
                break

        properties = self.indexToByte(self.index, propertyLength)
        self.parsePropertiesHelper(properties)
        self.index += propertyLength * 2


    # Given an index in the payload, return the corresponding
    # byte (or several bytes).
    def indexToByte(self, index = None, numBytes = 1, payload = None):
        if index is None:
            index = self.index
        if payload is None:
            payload = self.payload
        return payload[index:index+(numBytes * 2)]

    def __init__(self, payload, protocol_version):
        self.payload = payload
        self.protocol_version = protocol_version
        self.G_fields = {}
        self.H_fields = {}
        self.index = 0

        # Fixed header always goes in G fields
        fixed_header = self.indexToByte()
        self.G_fields["fixed header"] = fixed_header

        # Get the length
        self.index = 2
        self.remaining_length = payload[self.index:self.index+2]
        while int(self.indexToByte(), 16) > 127:
            self.index += 2
            self.remaining_length += payload[self.index:self.index+2]
        self.index += 2