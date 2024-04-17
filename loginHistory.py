# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import datetime
import random

from shc.interfaces.in_memory_data_logging import InMemoryDataLogVariable
import shc.web.log_widgets
from shc.data_logging import AggregationMethod
from shc.web.log_widgets import ChartDataSpec, LogListDataSpec
from shc.web.widgets import icon

random_float_log = InMemoryDataLogVariable(float, keep=datetime.timedelta(minutes=10))
random_bool_log = InMemoryDataLogVariable(bool, keep=datetime.timedelta(minutes=10))

# Some hacks to prefill logs with random data
ts = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=7.5)
while ts < datetime.datetime.now(datetime.timezone.utc):
    random_bool_log.data.append((ts, bool(random.getrandbits(1))))
    ts += datetime.timedelta(seconds=random.uniform(0.2, 90))
ts = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10)
while ts < datetime.datetime.now(datetime.timezone.utc):
    random_float_log.data.append((ts, random.uniform(0, 40)))
    ts += datetime.timedelta(seconds=random.uniform(0.2, 90))


# Now, generate new events at random intervals
@shc.timer.every(datetime.timedelta(seconds=20), random=datetime.timedelta(seconds=19.8))
@shc.handler()
async def new_float(_v, _o):
    await random_float_log.write(random.uniform(0, 40))


@shc.timer.every(datetime.timedelta(seconds=20), random=datetime.timedelta(seconds=19.8))
@shc.handler()
async def new_bool(_v, _o):
    await random_bool_log.write(bool(random.getrandbits(1)))


# The web server and web page
web_server = shc.web.WebServer('localhost', 8081, index_name='history')
history_page = web_server.page('history', 'history', menu_entry=True, menu_icon='home')


#############################################################################################
# Log list widget                                                                           #
#############################################################################################
history_page.add_item(shc.web.log_widgets.LogListWidget(datetime.timedelta(minutes=5), [
    LogListDataSpec(random_bool_log, format=lambda x: "on" if x else "off", color="teal"),
    LogListDataSpec(random_float_log),
]))


history_page.add_item(shc.web.log_widgets.LogListWidget(datetime.timedelta(minutes=5), [
    LogListDataSpec(random_bool_log, format="{:.2f} s", aggregation=AggregationMethod.ON_TIME)
]))

history_page.add_item(shc.web.log_widgets.LogListWidget(datetime.timedelta(minutes=5), [
    LogListDataSpec(random_float_log,
                    format=icon('thermometer', "{:.2f} °C"),
                    aggregation=AggregationMethod.AVERAGE)
]))

history_page.new_segment()

history_page.add_item(shc.web.log_widgets.ChartWidget(datetime.timedelta(minutes=5), [
    ChartDataSpec(random_float_log, "random float", scale_factor=10)
]))

history_page.add_item(shc.web.log_widgets.ChartWidget(datetime.timedelta(minutes=5), [
    ChartDataSpec(random_float_log, "avg", aggregation=AggregationMethod.AVERAGE, unit_symbol="°C"),
    ChartDataSpec(random_float_log, "min", aggregation=AggregationMethod.MINIMUM, unit_symbol="°C"),
    ChartDataSpec(random_float_log, "max", aggregation=AggregationMethod.MAXIMUM, unit_symbol="°C"),
]))


if __name__ == '__main__':
    shc.main()
