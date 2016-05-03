#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase, main
from pitchpx.mlbam_util import MlbamUtil, MlbAmHttpNotFound

__author__ = 'Shinichi Nakagawa'


class TestMlbamUtil(TestCase):
    """
    MLBAM Util Class Test
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_content_200(self):
        """
        Get html content(status:200, head:default)
        """
        req = MlbamUtil._get_content(
            'http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_lanmlb_sdnmlb_1/game.xml'
        )
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.request.headers['Accept'],
                         'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        self.assertEqual(req.request.headers['User-Agent'],
                         ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'))

    def test_get_content_200_setting_header(self):
        """
        Get html content(status:200, head:original)
        """
        req = MlbamUtil._get_content(
            'http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_lanmlb_sdnmlb_1/game.xml',
            headers={'Accept': 'text/html', 'User-Agent': 'Python-urllib/3.5'}
        )
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.request.headers['Accept'], 'text/html')
        self.assertEqual(req.request.headers['User-Agent'], 'Python-urllib/3.5')

    def test_get_content_404_setting_header(self):
        """
        Get html content(status:404, head:original)
        """
        req = MlbamUtil._get_content(
            'http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_chnmlb_anamlb_1/game.xml',
            headers={'Accept': 'text/html', 'User-Agent': 'Python-urllib/3.5'}
        )
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.request.headers['Accept'], 'text/html')
        self.assertEqual(req.request.headers['User-Agent'], 'Python-urllib/3.5')

    def test_find_xml_200(self):
        """
        Get xml content(status:200, head:default)
        """
        req = MlbamUtil.find_xml(
            'http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_lanmlb_sdnmlb_1/game.xml',
            'lxml',
        )
        self.assertIsNotNone(req)

    def test_find_xml_404(self):
        """
        Get xml content(status:404, head:default)
        """
        try:
            _ = MlbamUtil.find_xml(
                'http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_chnmlb_anamlb_1/game.xml',
                'lxml',
            )
        except MlbAmHttpNotFound as e:
            self.assertEqual(
                e.msg,
                ('HTTP Error '
                 'url: http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_06/gid_2016_04_06_chnmlb_anamlb_1/game.xml '
                 'status: 404'
                 )
            )


if __name__ == '__main__':
    main()