from unittest import TestCase, main

import mentorTask10.list_generator
from mentorTask10.mongo_actions import import_entity, import_entities, lazy_update, get_data_slice, clear_db
import pymongo
import datetime as dt
from mentorTask10.list_generator import generate_list_of_entities, generate_list_of_n_entities, START_DATE, END_DATE
from mentorTask10.cl_currency import ClCurrency
from mentorTask10.cl_daily_bar import ClDailyBar



client = pymongo.MongoClient("localhost:27017")
db = client.cl_daily_bars
coll = db.Tests


class MongoActionsTest(TestCase):
    def test_import_entity_value_check(self):
        clear_db(coll)
        e = ClDailyBar(dt.datetime(2000, 1, 1), 2305.0, "Dell", ClCurrency.F_E_CHF)
        import_entity(e, coll)
        self.assertEqual(coll.find_one({'AssetName': 'Dell'})['Value'], 2305)

    def test_import_entities_value_check(self):
        clear_db(coll)
        e = ClDailyBar(dt.datetime(2000, 1, 1), 2305.0, "Dell", ClCurrency.F_E_CHF)
        e1 = ClDailyBar(dt.datetime(2001, 1, 1), 2325.0, "Doll", ClCurrency.F_E_CHF)

        import_entities([e, e1], coll)

        self.assertEqual(coll.find_one({'AssetName': 'Dell'})['Value'], 2305)

    def test_import_entities_len_check(self):
        clear_db(coll)
        st_y = 2000
        e_y = 2000
        st_m = 1
        e_m = 1
        st_d = 2
        e_d = 20
        l = generate_list_of_entities(3, st_y=st_y, e_y=e_y, st_m=st_m, e_m=e_m, st_d=st_d, e_d=e_d)

        import_entities(l, coll)

        self.assertEqual(len(list(coll.find({}))), e_d - st_d + 1)

    def test_lazy_update_value_check(self):
        clear_db(coll)
        e = ClDailyBar(dt.datetime(2000, 1, 1), 2305.0, "Dell", ClCurrency.F_E_CHF)
        e1 = ClDailyBar(dt.datetime(2001, 1, 1), 2325.0, "Doll", ClCurrency.F_E_CHF)
        l = [e, e1]
        import_entities(l, coll)
        lazy_update(e, {'AssetName': 'Cell'}, coll=coll)

        self.assertEqual(coll.find_one({'AssetName': 'Cell'})['Value'], 2305)

    def test_lazy_update_len_check(self):
        clear_db(coll)
        e = ClDailyBar(dt.datetime(2000, 1, 1), 2305.0, "Dell", ClCurrency.F_E_CHF)
        e1 = ClDailyBar(dt.datetime(2001, 1, 1), 2325.0, "Doll", ClCurrency.F_E_CHF)
        l = [e, e1]
        import_entities(l, coll)
        lazy_update(e, {'AssetName': 'Cell'}, coll=coll)

        self.assertEqual(len(list(coll.find({}))), len(l))

    def test_lazy_update_laziness_check(self):
        clear_db(coll)
        e = ClDailyBar(dt.datetime(2000, 1, 1), 2305.0, "Dell", ClCurrency.F_E_CHF)
        e1 = ClDailyBar(dt.datetime(2001, 1, 1), 2325.0, "Doll", ClCurrency.F_E_CHF)
        l = [e, e1]
        import_entities(l, coll)
        id_of_entity = coll.find_one({'AssetName': 'Dell'})['_id']
        lazy_update(e, {'AssetName': 'Dell'}, coll=coll)

        self.assertEqual(coll.find_one({'AssetName': 'Dell'})['_id'], id_of_entity)

    def test_get_data_slice_len_test(self):
        clear_db(coll)
        le = 60
        import_entities(generate_list_of_n_entities(le), coll)
        l = get_data_slice(mentorTask10.list_generator.ASSETS[1], coll=coll)
        self.assertEqual(len(l), int((le - 1) / len(mentorTask10.list_generator.ASSETS.items()) + 1))

    def test_get_data_slice_type_test(self):
        clear_db(coll)
        le = 60
        import_entities(generate_list_of_n_entities(le), coll)
        l = get_data_slice(mentorTask10.list_generator.ASSETS[1], coll=coll)
        self.assertEqual(type(l), type([]))

    def test_get_data_slice_data_correctness_test(self):
        clear_db(coll)
        le = 60
        import_entities(generate_list_of_n_entities(le), coll)
        e_d = END_DATE - dt.timedelta(days=1)
        s_d = START_DATE + dt.timedelta(days=1)
        l = get_data_slice(mentorTask10.list_generator.ASSETS[1], from_date=s_d,
                           to_date=e_d, coll=coll)
        for i in l:
            with self.subTest(i=i):
                self.assertGreaterEqual(e_d, i.date)
                self.assertLessEqual(s_d, i.date)
