# coding=utf-8
# Copyright 2022 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for color_miner.py."""

from typing import Any, Dict, List, Optional
from unittest import mock

from absl.testing import parameterized

import constants
from util import app_util
from util import color_miner


def _build_dummy_product(
    properties_to_be_updated: Optional[Dict[str, Any]] = None,
    properties_to_be_removed: Optional[List[str]] = None) -> Dict[str, Any]:
  """Builds a dummy product data.

  Args:
    properties_to_be_updated: The properties of a product and their values to be
      updated in a request body.
    properties_to_be_removed: The properties of a product that should be
      removed.

  Returns:
    A dummy product data.
  """
  product = {
      'color': '',
      'title': '',
      'description': '',
      'googleProductCategory': 'Apparel & Accessories',
  }

  if properties_to_be_updated:
    for key, value in properties_to_be_updated.items():
      product[key] = value

  if properties_to_be_removed:
    for key in properties_to_be_removed:
      if key in product:
        del product[key]

  return product


@mock.patch('util.color_miner._COLOR_OPTIMIZER_CONFIG_FILE_NAME',
            'color_optimizer_config_{}_test')
@mock.patch(
    'util.color_miner._GPC_STRING_TO_ID_MAPPING_CONFIG_FILE_NAME',
    'gpc_string_to_id_mapping_{}_test')
class ColorMinerTest(parameterized.TestCase):

  def setUp(self):
    super(ColorMinerTest, self).setUp()
    app_util.setup_test_app()

  @parameterized.named_parameters([
      {
          'testcase_name':
              'mines_from_color',
          'product':
              _build_dummy_product(properties_to_be_updated={'color': '???'}),
          'expected_standard_colors': ['???'],
          'expected_unique_colors': ['???']
      },
      {
          'testcase_name':
              'mines_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': '???????????????????????????'
                  }),
          'expected_standard_colors': ['?????????'],
          'expected_unique_colors': ['?????????']
      },
      {
          'testcase_name':
              'mines_two_colors_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': '????????????????????????????????????'
                  }),
          'expected_standard_colors': ['?????????', '????????????'],
          'expected_unique_colors': ['?????????', '????????????']
      },
      {
          'testcase_name':
              'mines_three_colors_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title':
                          '????????????????????????????????????????????????'
                  }),
          'expected_standard_colors': [
              '?????????', '????????????', '?????????'
          ],
          'expected_unique_colors': ['?????????', '????????????', '?????????']
      },
      {
          'testcase_name':
              'mines_from_description',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': '',
                      'description': '???????????????'
                  }),
          'expected_standard_colors': ['???'],
          'expected_unique_colors': ['???']
      },
  ])
  def test_mine_color_mines_color_with_language_ja(self, product,
                                                   expected_standard_colors,
                                                   expected_unique_colors):
    miner = color_miner.ColorMiner(language='ja')

    mined_standard_color, mined_unique_color = miner.mine_color(product)

    self.assertCountEqual(expected_standard_colors, mined_standard_color)
    self.assertCountEqual(expected_unique_colors, mined_unique_color)

  @parameterized.named_parameters([
      {
          'testcase_name':
              'mines_from_color',
          'product':
              _build_dummy_product(properties_to_be_updated={'color': 'Blue'}),
          'expected_standard_colors': ['Blue'],
          'expected_unique_colors': ['Blue']
      },
      {
          'testcase_name':
              'mines_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={'title': 'Title Red'}),
          'expected_standard_colors': ['Red'],
          'expected_unique_colors': ['Red']
      },
      {
          'testcase_name':
              'mines_two_colors_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={'title': 'Title Red Green'}),
          'expected_standard_colors': ['Red', 'Green'],
          'expected_unique_colors': ['Red', 'Green']
      },
      {
          'testcase_name':
              'mines_from_description',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': '',
                      'description': 'Description Green'
                  }),
          'expected_standard_colors': ['Green'],
          'expected_unique_colors': ['Green']
      },
  ])
  def test_mine_color_mines_color_with_language_en(self, product,
                                                   expected_standard_colors,
                                                   expected_unique_colors):
    miner = color_miner.ColorMiner(language=constants.LANGUAGE_CODE_EN)

    mined_standard_color, mined_unique_color = miner.mine_color(product)

    self.assertCountEqual(expected_standard_colors, mined_standard_color)
    self.assertCountEqual(expected_unique_colors, mined_unique_color)

  @parameterized.named_parameters([
      {
          'testcase_name':
              'mines_from_color',
          'product':
              _build_dummy_product(
                  properties_to_be_updated={'color': 'xanh n?????c bi???n'}),
          'expected_standard_colors': ['xanh n?????c bi???n'],
          'expected_unique_colors': ['xanh n?????c bi???n'],
      },
      {
          'testcase_name':
              'mines_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={'title': 'Title m??u ?????'}),
          'expected_standard_colors': ['M??u ?????'],
          'expected_unique_colors': ['M??u ?????'],
      },
      {
          'testcase_name':
              'mines_two_colors_from_title',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': 'Title m??u ????? xanh l?? c??y',
                  }),
          'expected_standard_colors': ['M??u ?????', 'Xanh L?? C??y'],
          'expected_unique_colors': ['M??u ?????', 'Xanh L?? C??y'],
      },
      {
          'testcase_name':
              'mines_from_description',
          'product':
              _build_dummy_product(
                  properties_to_be_removed=['color'],
                  properties_to_be_updated={
                      'title': '',
                      'description': 'Description xanh l?? c??y',
                  }),
          'expected_standard_colors': ['Xanh L?? C??y'],
          'expected_unique_colors': ['Xanh L?? C??y'],
      },
  ])
  def test_mine_color_mines_color_with_language_vi(self, product,
                                                   expected_standard_colors,
                                                   expected_unique_colors):
    miner = color_miner.ColorMiner(language='vi')

    mined_standard_color, mined_unique_color = miner.mine_color(product)

    self.assertCountEqual(expected_standard_colors, mined_standard_color)
    self.assertCountEqual(expected_unique_colors, mined_unique_color)

  def test_mine_color_mines_three_colors_from_title_including_four_colors(self):
    miner = color_miner.ColorMiner(language='ja')
    product = _build_dummy_product(
        properties_to_be_removed=['color'],
        properties_to_be_updated={
            'title':
                '??????????????????????????????????????????????????????????????????'
        })

    mined_standard_color, mined_unique_color = miner.mine_color(product)

    self.assertLen(mined_standard_color, 3)
    self.assertLen(mined_unique_color, 3)

  @parameterized.named_parameters([{
      'testcase_name': 'string',
      'category': 'Software'
  }, {
      'testcase_name': 'number',
      'category': '123456'
  }])
  def test_mine_color_does_not_mine_from_text_when_google_product_category_is_invalid(
      self, category):
    product = _build_dummy_product(
        properties_to_be_removed=['color'],
        properties_to_be_updated={
            'title': '?????????????????????',
            'description': '?????????',
            'googleProductCategory': category
        })

    miner = color_miner.ColorMiner(language='ja')

    mined_standard_color, mined_unique_color = miner.mine_color(product)

    self.assertIsNone(mined_standard_color)
    self.assertIsNone(mined_unique_color)
