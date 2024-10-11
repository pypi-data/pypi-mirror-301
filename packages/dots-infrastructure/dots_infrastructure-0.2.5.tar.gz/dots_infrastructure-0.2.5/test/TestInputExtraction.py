import unittest
import base64
import helics as h

from dots_infrastructure.EsdlHelper import EsdlHelper
from dots_infrastructure.DataClasses import CalculationServiceInput, SubscriptionDescription

class TestParse(unittest.TestCase):

    def setUp(self):
        with open("test.esdl", mode="r") as esdl_file:
            self.encoded_base64_esdl = base64.b64encode(esdl_file.read().encode('utf-8')).decode('utf-8')

    def test_given_esdl_entity_recevies_subscriptions_from_connected_entities(self):

        # Arrange
        simulator_esdl_id = 'f006d594-0743-4de5-a589-a6c2350898da'

        esdl_helper = EsdlHelper(self.encoded_base64_esdl)

        subscription_descriptions = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE),
        ]

        expected_input_descriptions = [
            CalculationServiceInput("PVInstallation", "PV_Dispatch", '176af591-6d9d-4751-bb0f-fac7e99b1c3d', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch/176af591-6d9d-4751-bb0f-fac7e99b1c3d"),
            CalculationServiceInput("PVInstallation", "PV_Dispatch", 'b8766109-5328-416f-9991-e81a5cada8a6', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch/b8766109-5328-416f-9991-e81a5cada8a6")
        ]

        calculation_services = [
            "PVInstallation",
            "EnergyMarket"
        ]

        # Execute
        inputs = esdl_helper.get_connected_input_esdl_objects(simulator_esdl_id, calculation_services, subscription_descriptions)

        # Assert correct assets are extracted from esdl file
        self.assertListEqual(expected_input_descriptions, inputs)

    def test_given_esdl_entity_can_subscribe_to_non_connected_inputs(self):
        simulator_esdl_id = 'f006d594-0743-4de5-a589-a6c2350898da'

        esdl_helper = EsdlHelper(self.encoded_base64_esdl)

        subscription_descriptions = [
            SubscriptionDescription("EnergyMarket", "DA_Price", "EUR", h.HelicsDataType.DOUBLE)
        ]

        expected_input_descriptions = [
            CalculationServiceInput("EnergyMarket", "DA_Price", 'b612fc89-a752-4a30-84bb-81ebffc56b50', "EUR", h.HelicsDataType.DOUBLE, simulator_esdl_id, "EnergyMarket/DA_Price/b612fc89-a752-4a30-84bb-81ebffc56b50")
        ]

        calculation_services = [
            "EnergyMarket"
        ]

        # Execute
        inputs = esdl_helper.get_connected_input_esdl_objects(simulator_esdl_id, calculation_services, subscription_descriptions)

        # Assert correct assets are extracted from esdl file
        self.assertListEqual(expected_input_descriptions, inputs)

    def test_given_esdl_entity_has_two_publications_then_connected_entity_can_subscribe_to_both(self):

        # Arrange

        simulator_esdl_id = 'f006d594-0743-4de5-a589-a6c2350898da'

        esdl_helper = EsdlHelper(self.encoded_base64_esdl)

        subscription_descriptions = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE),
            SubscriptionDescription("PVInstallation", "PV_Dispatch2", "W", h.HelicsDataType.DOUBLE)
        ]

        expected_input_descriptions = [
            CalculationServiceInput("PVInstallation", "PV_Dispatch", '176af591-6d9d-4751-bb0f-fac7e99b1c3d', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch/176af591-6d9d-4751-bb0f-fac7e99b1c3d"),
            CalculationServiceInput("PVInstallation", "PV_Dispatch2", '176af591-6d9d-4751-bb0f-fac7e99b1c3d', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch2/176af591-6d9d-4751-bb0f-fac7e99b1c3d"),
            CalculationServiceInput("PVInstallation", "PV_Dispatch", 'b8766109-5328-416f-9991-e81a5cada8a6', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch/b8766109-5328-416f-9991-e81a5cada8a6"),
            CalculationServiceInput("PVInstallation", "PV_Dispatch2", 'b8766109-5328-416f-9991-e81a5cada8a6', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "PVInstallation/PV_Dispatch2/b8766109-5328-416f-9991-e81a5cada8a6"),
        ]

        calculation_services = [
            "PVInstallation"
        ]

        # Execute
        inputs = esdl_helper.get_connected_input_esdl_objects(simulator_esdl_id, calculation_services, subscription_descriptions)

        # Assert correct assets are extracted from esdl file
        self.assertListEqual(expected_input_descriptions, inputs)

    def test_given_non_energy_entity_subscriptions_are_correctly_extracted(self):
        # Arrange
        simulator_esdl_id = '02fafa20-a1bd-488e-a4db-f3c0ca7ff51a'

        esdl_helper = EsdlHelper(self.encoded_base64_esdl)

        subscription_descriptions = [
            SubscriptionDescription("EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        expected_input_descriptions = [
            CalculationServiceInput("EConnection", "EConnectionDispatch", 'f006d594-0743-4de5-a589-a6c2350898da', "W", h.HelicsDataType.DOUBLE, simulator_esdl_id, "EConnection/EConnectionDispatch/f006d594-0743-4de5-a589-a6c2350898da")
        ]

        calculation_services = [
            "EConnection"
        ]

        # Execute
        inputs = esdl_helper.get_connected_input_esdl_objects(simulator_esdl_id, calculation_services, subscription_descriptions)

        # Assert correct assets are extracted from esdl file
        self.assertListEqual(expected_input_descriptions, inputs)

if __name__ == '__main__':
    unittest.main()