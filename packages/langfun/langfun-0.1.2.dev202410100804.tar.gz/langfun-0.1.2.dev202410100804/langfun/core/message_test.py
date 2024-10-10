# Copyright 2023 The Langfun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for message."""

import inspect
import unittest
from langfun.core import message
from langfun.core import modality
import pyglove as pg


class CustomModality(modality.Modality):
  content: str

  def to_bytes(self):
    return self.content.encode()

  def _repr_html_(self):
    return f'<div>CustomModality: {self.content}</div>'


class MessageTest(unittest.TestCase):

  def test_basics(self):

    class A(pg.Object):
      pass

    d = pg.Dict(x=A())

    m = message.UserMessage('hi', metadata=dict(x=1), x=pg.Ref(d.x), y=2)
    self.assertEqual(m.metadata, {'x': pg.Ref(d.x), 'y': 2})
    self.assertEqual(m.sender, 'User')
    self.assertIs(m.x, d.x)
    self.assertEqual(m.y, 2)

    with self.assertRaises(AttributeError):
      _ = m.z
    self.assertEqual(hash(m), hash(m.text))
    del d

  def test_from_value(self):
    self.assertTrue(
        pg.eq(message.UserMessage.from_value('hi'), message.UserMessage('hi'))
    )
    self.assertTrue(
        pg.eq(
            message.UserMessage.from_value(CustomModality('foo')),
            message.UserMessage('<<[[object]]>>', object=CustomModality('foo')),
        )
    )
    m = message.UserMessage('hi')
    self.assertIs(message.UserMessage.from_value(m), m)

  def test_source_tracking(self):
    m1 = message.UserMessage('hi')
    m1.tag('lm-input')
    self.assertIsNone(m1.source)
    self.assertIs(m1.root, m1)

    m2 = message.UserMessage('foo', source=m1)
    m2.source = m1
    self.assertIs(m2.source, m1)
    self.assertIs(m2.root, m1)
    m2.tag('lm-response')

    m3 = message.UserMessage('bar', source=m2)
    self.assertIs(m3.source, m2)
    self.assertIs(m3.root, m1)
    m3.tag('transformed')
    m3.tag('lm-output')

    self.assertEqual(
        m3.trace(), [m1, m2, m3],
    )
    self.assertEqual(
        m3.trace('lm-input'), [m1]
    )
    self.assertEqual(
        m3.trace('transformed'), [m3]
    )
    self.assertIs(m2.lm_input, m1)
    self.assertIs(m3.lm_input, m1)
    self.assertEqual(m3.lm_inputs, [m1])
    self.assertIs(m2.lm_response, m2)
    self.assertIs(m3.lm_response, m2)
    self.assertEqual(m3.lm_responses, [m2])
    self.assertIs(m3.lm_output, m3)
    self.assertEqual(m3.lm_outputs, [m3])
    self.assertIsNone(m3.last('non-exist'))

  def test_result(self):
    m = message.UserMessage('hi', x=1, y=2)
    self.assertIsNone(m.result)
    m.result = 1
    self.assertEqual(m.result, 1)

  def test_jsonify(self):
    m = message.UserMessage('hi', result=1)
    self.assertEqual(pg.from_json_str(m.to_json_str()), m)

  def test_get(self):

    class A(pg.Object):
      p: int

    # Create a symbolic object and assign it to a container, so we could test
    # pg.Ref.
    a = A(1)
    d = pg.Dict(x=a)

    m = message.UserMessage('hi', x=pg.Ref(a), y=dict(z=[0, 1, 2]))
    self.assertEqual(m.get('text'), 'hi')
    self.assertIs(m.get('x'), a)
    self.assertIs(m.get('x.p'), 1)
    self.assertEqual(m.get('y'), dict(z=[0, 1, 2]))
    self.assertEqual(m.get('y.z'), [0, 1, 2])
    self.assertEqual(m.get('y.z[0]'), 0)
    self.assertIsNone(m.get('p'))
    self.assertEqual(m.get('p', default='foo'), 'foo')
    del d

  def test_set(self):
    m = message.UserMessage('hi', metadata=dict(x=1, z=0))
    m.set('text', 'hello')
    m.set('x', 2)
    m.set('y', [0, 1, 2])
    m.set('y[0]', 1)
    m.set('y[2]', pg.MISSING_VALUE)  # delete `y[2]`.
    m.set('z', pg.MISSING_VALUE)  # delete `z`.
    self.assertEqual(
        m, message.UserMessage('hello', metadata=dict(x=2, y=[1, 1]))
    )

  def test_updates(self):
    m = message.UserMessage('hi')
    self.assertFalse(m.modified)
    self.assertFalse(m.has_errors)

    with m.update_scope():
      m.metadata.x = 1
      m.metadata.y = 1
      self.assertTrue(m.modified)
      self.assertEqual(len(m.updates), 2)
      self.assertFalse(m.has_errors)

      with m.update_scope():
        m.metadata.y = 2
        m.metadata.z = 2
        m.errors.append(ValueError('b'))
        self.assertTrue(m.modified)
        self.assertEqual(len(m.updates), 2)
        self.assertTrue(m.has_errors)
        self.assertEqual(len(m.errors), 1)

        with m.update_scope():
          self.assertFalse(m.modified)
          self.assertFalse(m.has_errors)

    self.assertTrue(m.modified)
    self.assertEqual(len(m.updates), 3)
    self.assertTrue(m.has_errors)
    self.assertEqual(len(m.errors), 1)

    m2 = message.UserMessage('hi')
    m2.apply_updates(m.updates)
    self.assertEqual(m, m2)

  def test_user_message(self):
    m = message.UserMessage('hi')
    self.assertEqual(m.text, 'hi')
    self.assertEqual(m.sender, 'User')
    self.assertTrue(m.from_user)
    self.assertFalse(m.from_agent)
    self.assertFalse(m.from_system)
    self.assertFalse(m.from_memory)
    self.assertEqual(str(m), m.text)

    m = message.UserMessage('hi', sender='Tom')
    self.assertEqual(m.sender, 'Tom')
    self.assertEqual(str(m), m.text)

  def test_ai_message(self):
    m = message.AIMessage('hi')
    self.assertEqual(m.text, 'hi')
    self.assertEqual(m.sender, 'AI')
    self.assertFalse(m.from_user)
    self.assertTrue(m.from_agent)
    self.assertFalse(m.from_system)
    self.assertFalse(m.from_memory)
    self.assertEqual(str(m), m.text)

    m = message.AIMessage('hi', sender='Model')
    self.assertEqual(m.sender, 'Model')
    self.assertEqual(str(m), m.text)

  def test_system_message(self):
    m = message.SystemMessage('hi')
    self.assertEqual(m.text, 'hi')
    self.assertEqual(m.sender, 'System')
    self.assertFalse(m.from_user)
    self.assertFalse(m.from_agent)
    self.assertTrue(m.from_system)
    self.assertFalse(m.from_memory)
    self.assertEqual(str(m), m.text)

    m = message.SystemMessage('hi', sender='Environment1')
    self.assertEqual(m.sender, 'Environment1')
    self.assertEqual(str(m), m.text)

  def test_memory_record(self):
    m = message.MemoryRecord('hi')
    self.assertEqual(m.text, 'hi')
    self.assertEqual(m.sender, 'Memory')
    self.assertFalse(m.from_user)
    self.assertFalse(m.from_agent)
    self.assertFalse(m.from_system)
    self.assertTrue(m.from_memory)
    self.assertEqual(str(m), m.text)

    m = message.MemoryRecord('hi', sender="Someone's Memory")
    self.assertEqual(m.sender, 'Someone\'s Memory')
    self.assertEqual(str(m), m.text)

  def test_get_modality(self):
    m1 = message.UserMessage(
        'hi, this is a {{img1}} and {{x.img2}}',
        img1=CustomModality('foo'),
        x=dict(img2=pg.Ref(CustomModality('bar'))),
    )
    self.assertIs(m1.get_modality('img1'), m1.img1)
    self.assertIs(m1.get_modality('x.img2'), m1.x.img2)
    self.assertIsNone(m1.get_modality('video'))

    m2 = message.SystemMessage('class Question:\n  image={{img1}}', source=m1)
    self.assertIs(m2.get_modality('img1'), m1.img1)
    # We could get the modality object even it's not directly used by current
    # message.
    self.assertIs(m2.get_modality('x.img2'), m1.x.img2)
    self.assertIsNone(m2.get_modality('video'))

    m3 = message.AIMessage(
        'This is the {{output_image}} based on {{x.img2}}',
        output_image=CustomModality('bar'),
        source=m2,
    )
    self.assertIs(m3.get_modality('x.img2'), m1.x.img2)
    self.assertIs(m3.get_modality('output_image'), m3.output_image)
    self.assertIsNone(m3.get_modality('video'))

  def test_referred_modalities(self):
    m1 = message.UserMessage(
        'hi, this is a <<[[img1]]>> and <<[[x.img2]]>>',
        img1=CustomModality('foo'),
        x=dict(img2=CustomModality('bar')),
    )
    m2 = message.SystemMessage('class Question:\n  image={{img1}}', source=m1)
    m3 = message.AIMessage(
        (
            'This is the <<[[output_image]]>> based on <<[[x.img2]]>>, '
            '{{unknown_var}}'
        ),
        output_image=CustomModality('bar'),
        source=m2,
    )
    self.assertEqual(
        m3.referred_modalities(),
        {
            'output_image': m3.output_image,
            'x.img2': m1.x.img2,
        },
    )

  def test_text_with_modality_hash(self):
    m = message.UserMessage(
        'hi, this is a <<[[img1]]>> and <<[[x.img2]]>>',
        img1=CustomModality('foo'),
        x=dict(img2=CustomModality('bar')),
    )
    self.assertEqual(
        m.text_with_modality_hash,
        (
            'hi, this is a <<[[img1]]>> and <<[[x.img2]]>>'
            '<img1>acbd18db</img1><x.img2>37b51d19</x.img2>'
        )
    )

  def test_chunking(self):
    m = message.UserMessage(
        inspect.cleandoc("""
            Hi, this is <<[[a]]>> and this is {{b}}.
            <<[[x.c]]>> {{something else
            """),
        a=CustomModality('foo'),
        x=dict(c=CustomModality('bar')),
    )
    chunks = m.chunk()
    self.assertTrue(
        pg.eq(
            chunks,
            [
                'Hi, this is',
                CustomModality('foo'),
                'and this is {{b}}.\n',
                CustomModality('bar'),
                '{{something else',
            ],
        )
    )
    self.assertTrue(
        pg.eq(
            message.AIMessage.from_chunks(chunks),
            message.AIMessage(
                inspect.cleandoc("""
                    Hi, this is <<[[obj0]]>> and this is {{b}}.
                    <<[[obj1]]>> {{something else
                    """),
                obj0=pg.Ref(m.a),
                obj1=pg.Ref(m.x.c),
            ),
        )
    )

  def test_html(self):
    m = message.UserMessage(
        'hi, this is a <<[[img1]]>> and <<[[x.img2]]>>',
        img1=CustomModality('foo'),
        x=dict(img2=CustomModality('bar')),
    )
    self.assertEqual(
        m._repr_html_(),
        (
            '<div style="padding:0px 10px 0px 10px;"><span style="color: white;'
            'background-color: green;display:inline-block; border-radius:10px; '
            'padding:5px; margin-top: 5px; margin-bottom: 5px; white-space: '
            'pre-wrap">UserMessage</span><hr><span style="color: green; '
            'white-space: pre-wrap;">hi, this is a&nbsp;<span style="color: '
            'black;background-color: #f7dc6f;display:inline-block; '
            'border-radius:10px; padding:5px; margin-top: 5px; margin-bottom: '
            '5px; white-space: pre-wrap">img1</span>&nbsp;and&nbsp;<span style'
            '="color: black;background-color: #f7dc6f;display:inline-block; '
            'border-radius:10px; padding:5px; margin-top: 5px; margin-bottom: '
            '5px; white-space: pre-wrap">x.img2</span>&nbsp;</span><div style='
            '"padding-left: 20px; margin-top: 10px"><table style="border-top: '
            '1px solid #EEEEEE;"><tr><td style="padding: 5px; vertical-align: '
            'top; border-bottom: 1px solid #EEEEEE"><span style="color: black;'
            'background-color: #f7dc6f;display:inline-block; border-radius:'
            '10px; padding:5px; margin-top: 5px; margin-bottom: 0px; '
            'white-space: pre-wrap">img1</span></td><td style="padding: 15px '
            '5px 5px 5px; vertical-align: top; border-bottom: 1px solid '
            '#EEEEEE;"><div>CustomModality: foo</div></td></tr><tr><td style='
            '"padding: 5px; vertical-align: top; border-bottom: 1px solid '
            '#EEEEEE"><span style="color: black;background-color: #f7dc6f;'
            'display:inline-block; border-radius:10px; padding:5px; margin-top:'
            ' 5px; margin-bottom: 0px; white-space: pre-wrap">x.img2</span>'
            '</td><td style="padding: 15px 5px 5px 5px; vertical-align: top; '
            'border-bottom: 1px solid #EEEEEE;"><div>CustomModality: bar</div>'
            '</td></tr></table></div></div>'
        )
    )
    self.assertIn(
        'background-color: blue',
        message.AIMessage('hi').to_html().content,
    )
    self.assertIn(
        'background-color: black',
        message.SystemMessage('hi').to_html().content,
    )


if __name__ == '__main__':
  unittest.main()
