from packet import Packet
import random

class Properties(Packet):

    def conditionalAppend(self, whitelist, code, packet):
        if whitelist is None or code in whitelist:
            self.appendPayloadRandomly(packet)

    def __init__(self, whitelist = None):
        super().__init__()

        self.payload_format_indicator = self.toBinaryData(0x01, 1, True)
        self.conditionalAppend(whitelist, 0x01, self.payload_format_indicator)

        self.message_expiry_interval = self.toBinaryData(0x02, 4, True)
        self.conditionalAppend(whitelist, 0x02, self.message_expiry_interval)

        self.content_type_length = random.randint(0, 30)
        self.content_type = self.toEncodedString(0x03, self.content_type_length)
        self.conditionalAppend(whitelist, 0x03, self.content_type)

        self.response_topic_length = random.randint(0, 30)
        self.response_topic = self.toEncodedString(0x08, self.response_topic_length)
        self.conditionalAppend(whitelist, 0x08, self.response_topic)

        self.correlation_data_length = random.randint(0, 30)
        self.correlation_data = self.toBinaryData(0x09, self.correlation_data_length)
        self.conditionalAppend(whitelist, 0x09, self.correlation_data)

        self.subscription_identifier_value = random.randint(0, 268435455)
        self.subscription_identifier = "0b" + self.toVariableByte("%x" % self.subscription_identifier_value)
        self.conditionalAppend(whitelist, 0x0b, self.subscription_identifier)

        self.session_expiry_interval = self.toBinaryData(0x11, 4, True)
        self.conditionalAppend(whitelist, 0x11, self.session_expiry_interval)

        self.assigned_client_identifier_length = random.randint(0, 30)
        self.assigned_client_identifier = self.toEncodedString(0x12, self.assigned_client_identifier_length)
        self.conditionalAppend(whitelist, 0x12, self.assigned_client_identifier)

        self.server_keepalive = self.toBinaryData(0x13, 2, True)
        self.conditionalAppend(whitelist, 0x13, self.server_keepalive)

        self.authentication_method_len = random.randint(0, 30)
        self.authentication_method = self.toEncodedString(0x15, self.authentication_method_len)
        self.conditionalAppend(whitelist, 0x15, self.authentication_method)

        self.authentication_data_len = random.randint(0, 30)
        self.authentication_data = self.toEncodedString(0x16, self.authentication_data_len)
        self.conditionalAppend(whitelist, 0x16, self.authentication_data)

        self.request_problem_information = self.toBinaryData(0x17, 1, True, 1)
        self.conditionalAppend(whitelist, 0x17, self.request_problem_information)

        self.will_delay_interval = self.toBinaryData(0x18, 4, True)
        self.conditionalAppend(whitelist, 0x18, self.will_delay_interval)

        self.request_response_information = self.toBinaryData(0x19, 1, True, 1)
        self.conditionalAppend(whitelist, 0x19, self.request_response_information)

        self.response_information_length = random.randint(1, 30)
        self.response_information = self.toEncodedString(0x1a, self.response_information_length)
        self.conditionalAppend(whitelist, 0x1a, self.response_information)

        self.server_reference_length = random.randint(1, 30)
        self.server_reference = self.toEncodedString(0x1c, self.server_reference_length)
        self.conditionalAppend(whitelist, 0x1c, self.server_reference)

        self.reason_string_length = random.randint(1, 30)
        self.reason_string = self.toEncodedString(0x1f, self.reason_string_length)
        self.conditionalAppend(whitelist, 0x1f, self.reason_string)

        self.receive_maximum = self.toBinaryData(0x21, 2, True, 8, 1)
        self.conditionalAppend(whitelist, 0x21, self.receive_maximum)

        self.topic_alias_maximum = self.toBinaryData(0x22, 2, True)
        self.conditionalAppend(whitelist, 0x22, self.topic_alias_maximum)

        self.topic_alias = self.toBinaryData(0x23, 2, True)
        self.conditionalAppend(whitelist, 0x23, self.topic_alias)

        self.maximum_qos = self.toBinaryData(0x24, 1, True, 1)
        self.conditionalAppend(whitelist, 0x24, self.maximum_qos)

        self.retain_available = self.toBinaryData(0x25, 1, True, 1)
        self.conditionalAppend(whitelist, 0x25, self.retain_available)

        self.user_property_name_length = random.randint(1, 30)
        self.user_property_value_length = random.randint(1, 30)
        self.user_property = self.toEncodedStringPair(0x26, self.user_property_name_length, self.user_property_value_length)
        self.conditionalAppend(whitelist, 0x26, self.user_property)

        self.maximum_packet_size = self.toBinaryData(0x27, 4, True, 8, 1)
        self.conditionalAppend(whitelist, 0x27, self.maximum_packet_size)

        self.wildcard_subscription_available = self.toBinaryData(0x28, 1, True, 1)
        self.conditionalAppend(whitelist, 0x28, self.wildcard_subscription_available)

        self.subscription_identifiers_available = self.toBinaryData(0x29, 1, True, 1)
        self.conditionalAppend(whitelist, 0x29, self.subscription_identifiers_available)

        self.shared_subscription_available = self.toBinaryData(0x2a, 1, True, 1)
        self.conditionalAppend(whitelist, 0x2a, self.shared_subscription_available)

        self.prependPayloadLength()