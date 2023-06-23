import {gql, useQuery} from '@apollo/client';
import {
  Alert,
  Box,
  Button,
  Colors,
  Dialog,
  DialogFooter,
  Heading,
  NonIdealState,
  PageHeader,
  Spinner,
  TextInput,
  Tooltip,
} from '@dagster-io/ui';
import * as React from 'react';

import {PYTHON_ERROR_FRAGMENT} from '../app/PythonErrorFragment';
import {PythonErrorInfo} from '../app/PythonErrorInfo';
import {useQueryRefreshAtInterval, FIFTEEN_SECONDS} from '../app/QueryRefresh';
import {useTrackPageView} from '../app/analytics';
import {useDocumentTitle} from '../hooks/useDocumentTitle';
import {useQueryPersistedState} from '../hooks/useQueryPersistedState';
import {useSelectionReducer} from '../hooks/useSelectionReducer';
import {INSTANCE_HEALTH_FRAGMENT} from '../instance/InstanceHealthFragment';
import {RepoFilterButton} from '../instance/RepoFilterButton';
import {INSTIGATION_STATE_FRAGMENT} from '../instigation/InstigationUtils';
import {UnloadableSensors} from '../instigation/Unloadable';
import {filterPermissionedInstigationState} from '../instigation/filterPermissionedInstigationState';
import {SensorBulkActionMenu} from '../sensors/SensorBulkActionMenu';
import {SensorInfo} from '../sensors/SensorInfo';
import {makeSensorKey} from '../sensors/makeSensorKey';
import {CheckAllBox} from '../ui/CheckAllBox';
import {WorkspaceContext} from '../workspace/WorkspaceContext';
import {buildRepoAddress} from '../workspace/buildRepoAddress';
import {repoAddressAsHumanString} from '../workspace/repoAddressAsString';
import {RepoAddress} from '../workspace/types';

import {BASIC_INSTIGATION_STATE_FRAGMENT} from './BasicInstigationStateFragment';
import {OverviewSensorTable} from './OverviewSensorsTable';
import {OverviewTabs} from './OverviewTabs';
import {sortRepoBuckets} from './sortRepoBuckets';
import {BasicInstigationStateFragment} from './types/BasicInstigationStateFragment.types';
import {
  OverviewSensorsQuery,
  OverviewSensorsQueryVariables,
  UnloadableSensorsQuery,
  UnloadableSensorsQueryVariables,
} from './types/OverviewSensorsRoot.types';
import {visibleRepoKeys} from './visibleRepoKeys';

export const OverviewSensorsRoot = () => {
  useTrackPageView();
  useDocumentTitle('Visão Geral | Sensores');

  const {allRepos, visibleRepos} = React.useContext(WorkspaceContext);
  const repoCount = allRepos.length;
  const [searchValue, setSearchValue] = useQueryPersistedState<string>({
    queryKey: 'search',
    defaults: {search: ''},
  });

  const queryResultOverview = useQuery<OverviewSensorsQuery, OverviewSensorsQueryVariables>(
    OVERVIEW_SENSORS_QUERY,
    {
      fetchPolicy: 'network-only',
      notifyOnNetworkStatusChange: true,
    },
  );
  const {data, loading} = queryResultOverview;

  const refreshState = useQueryRefreshAtInterval(queryResultOverview, FIFTEEN_SECONDS);

  const repoBuckets = React.useMemo(() => {
    const visibleKeys = visibleRepoKeys(visibleRepos);
    return buildBuckets(data).filter(({repoAddress}) =>
      visibleKeys.has(repoAddressAsHumanString(repoAddress)),
    );
  }, [data, visibleRepos]);

  const sanitizedSearch = searchValue.trim().toLocaleLowerCase();
  const anySearch = sanitizedSearch.length > 0;

  const filteredBySearch = React.useMemo(() => {
    const searchToLower = sanitizedSearch.toLocaleLowerCase();
    return repoBuckets
      .map(({repoAddress, sensors}) => ({
        repoAddress,
        sensors: sensors.filter(({name}) => name.toLocaleLowerCase().includes(searchToLower)),
      }))
      .filter(({sensors}) => sensors.length > 0);
  }, [repoBuckets, sanitizedSearch]);

  const anySensorsVisible = React.useMemo(
    () => filteredBySearch.some(({sensors}) => sensors.length > 0),
    [filteredBySearch],
  );

  // Collect all sensors across visible code locations that the viewer has permission
  // to start or stop.
  const allPermissionedSensors = React.useMemo(() => {
    return repoBuckets
      .map(({repoAddress, sensors}) => {
        return sensors
          .filter(({sensorState}) => filterPermissionedInstigationState(sensorState))
          .map(({name, sensorState}) => ({
            repoAddress,
            sensorName: name,
            sensorState,
          }));
      })
      .flat();
  }, [repoBuckets]);

  // Build a list of keys from the permissioned schedules for use in checkbox state.
  // This includes collapsed code locations.
  const allPermissionedSensorKeys = React.useMemo(() => {
    return allPermissionedSensors.map(({repoAddress, sensorName}) =>
      makeSensorKey(repoAddress, sensorName),
    );
  }, [allPermissionedSensors]);

  const [{checkedIds: checkedKeys}, {onToggleFactory, onToggleAll}] = useSelectionReducer(
    allPermissionedSensorKeys,
  );

  // Filter to find keys that are visible given any text search.
  const permissionedKeysOnScreen = React.useMemo(() => {
    const filteredKeys = new Set(
      filteredBySearch
        .map(({repoAddress, sensors}) => {
          return sensors.map(({name}) => makeSensorKey(repoAddress, name));
        })
        .flat(),
    );
    return allPermissionedSensorKeys.filter((key) => filteredKeys.has(key));
  }, [allPermissionedSensorKeys, filteredBySearch]);

  // Determine the list of sensor objects that have been checked by the viewer.
  // These are the sensors that will be operated on by the bulk start/stop action.
  const checkedSensors = React.useMemo(() => {
    const checkedKeysOnScreen = new Set(
      permissionedKeysOnScreen.filter((key: string) => checkedKeys.has(key)),
    );
    return allPermissionedSensors.filter(({repoAddress, sensorName}) => {
      return checkedKeysOnScreen.has(makeSensorKey(repoAddress, sensorName));
    });
  }, [permissionedKeysOnScreen, allPermissionedSensors, checkedKeys]);

  const viewerHasAnyInstigationPermission = allPermissionedSensorKeys.length > 0;
  const checkedCount = checkedSensors.length;

  const content = () => {
    if (loading && !data) {
      return (
        <Box flex={{direction: 'row', justifyContent: 'center'}} style={{paddingTop: '100px'}}>
          <Box flex={{direction: 'row', alignItems: 'center', gap: 16}}>
            <Spinner purpose="body-text" />
            <div style={{color: Colors.Gray600}}>Loading sensors…</div>
          </Box>
        </Box>
      );
    }

    const anyReposHidden = allRepos.length > visibleRepos.length;

    if (!filteredBySearch.length) {
      if (anySearch) {
        return (
          <Box padding={{top: 20}}>
            <NonIdealState
              icon="search"
              title="No matching sensors"
              description={
                anyReposHidden ? (
                  <div>
                    No sensors matching <strong>{searchValue}</strong> were found in the selected
                    code locations
                  </div>
                ) : (
                  <div>
                    No sensors matching <strong>{searchValue}</strong> were found in your
                    definitions
                  </div>
                )
              }
            />
          </Box>
        );
      }

      return (
        <Box padding={{top: 20}}>
          <NonIdealState
            icon="search"
            title="Não há sensores"
            description={
              anyReposHidden
                ? 'Não foram encontrados sensores nos locais de código seleccionados'
                : 'Não foram encontrados sensores nas suas definições'
            }
          />
        </Box>
      );
    }

    return (
      <OverviewSensorTable
        headerCheckbox={
          viewerHasAnyInstigationPermission ? (
            <CheckAllBox
              checkedCount={checkedCount}
              totalCount={permissionedKeysOnScreen.length}
              onToggleAll={onToggleAll}
            />
          ) : undefined
        }
        repos={filteredBySearch}
        checkedKeys={checkedKeys}
        onToggleCheckFactory={onToggleFactory}
      />
    );
  };

  return (
    <Box flex={{direction: 'column'}} style={{height: '100%', overflow: 'hidden'}}>
      <PageHeader
        title={<Heading>Sensores</Heading>}
        tabs={<OverviewTabs tab="sensors" refreshState={refreshState} />}
      />
      <Box
        padding={{horizontal: 24, vertical: 16}}
        flex={{
          direction: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
          grow: 0,
        }}
      >
        <Box flex={{direction: 'row', gap: 12}}>
          {repoCount > 0 ? <RepoFilterButton /> : null}
          <TextInput
            icon="search"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            placeholder="Filtrar"
            style={{width: '340px'}}
          />
        </Box>
        <Tooltip
          content="You do not have permission to start or stop these schedules"
          canShow={anySensorsVisible && !viewerHasAnyInstigationPermission}
          placement="top-end"
          useDisabledButtonTooltipFix
        >
          <SensorBulkActionMenu sensors={checkedSensors} onDone={() => refreshState.refetch()} />
        </Tooltip>
      </Box>
      {loading && !repoCount ? (
        <Box padding={64}>
          <Spinner purpose="page" />
        </Box>
      ) : (
        <>
          {data?.unloadableInstigationStatesOrError.__typename === 'InstigationStates' ? (
            <UnloadableSensorsAlert
              count={data.unloadableInstigationStatesOrError.results.length}
            />
          ) : null}
          <SensorInfo
            daemonHealth={data?.instance.daemonHealth}
            padding={{vertical: 16, horizontal: 24}}
            border={{side: 'top', width: 1, color: Colors.KeylineGray}}
          />
          {content()}
        </>
      )}
    </Box>
  );
};

const UnloadableSensorsAlert: React.FC<{
  count: number;
}> = ({count}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  if (!count) {
    return null;
  }

  const title = count === 1 ? '1 unloadable sensor' : `${count} unloadable sensors`;

  return (
    <>
      <Box
        padding={{vertical: 16, horizontal: 24}}
        border={{side: 'top', width: 1, color: Colors.KeylineGray}}
      >
        <Alert
          intent="warning"
          title={title}
          description={
            <Box flex={{direction: 'column', gap: 12, alignItems: 'flex-start'}}>
              <div>
                Sensors were previously started but now cannot be loaded. They may be part of a code
                location that no longer exists. You can turn them off, but you cannot turn them back
                on.
              </div>
              <Button onClick={() => setIsOpen(true)}>
                {count === 1 ? 'View unloadable sensor' : 'View unloadable sensors'}
              </Button>
            </Box>
          }
        />
      </Box>
      <Dialog
        isOpen={isOpen}
        title="Unloadable schedules"
        style={{width: '90vw', maxWidth: '1200px'}}
      >
        <Box padding={{bottom: 8}}>
          <UnloadableSensorDialog />
        </Box>
        <DialogFooter>
          <Button intent="primary" onClick={() => setIsOpen(false)}>
            Done
          </Button>
        </DialogFooter>
      </Dialog>
    </>
  );
};

const UnloadableSensorDialog: React.FC = () => {
  const {data} = useQuery<UnloadableSensorsQuery, UnloadableSensorsQueryVariables>(
    UNLOADABLE_SENSORS_QUERY,
  );
  if (!data) {
    return <Spinner purpose="section" />;
  }

  if (data?.unloadableInstigationStatesOrError.__typename === 'InstigationStates') {
    return (
      <UnloadableSensors
        sensorStates={data.unloadableInstigationStatesOrError.results}
        showSubheading={false}
      />
    );
  }

  return <PythonErrorInfo error={data?.unloadableInstigationStatesOrError} />;
};

type RepoBucket = {
  repoAddress: RepoAddress;
  sensors: {name: string; sensorState: BasicInstigationStateFragment}[];
};

const buildBuckets = (data?: OverviewSensorsQuery): RepoBucket[] => {
  if (data?.workspaceOrError.__typename !== 'Workspace') {
    return [];
  }

  const entries = data.workspaceOrError.locationEntries.map((entry) => entry.locationOrLoadError);

  const buckets = [];

  for (const entry of entries) {
    if (entry?.__typename !== 'RepositoryLocation') {
      continue;
    }

    for (const repo of entry.repositories) {
      const {name, sensors} = repo;
      const repoAddress = buildRepoAddress(name, entry.name);

      if (sensors.length > 0) {
        buckets.push({
          repoAddress,
          sensors,
        });
      }
    }
  }

  return sortRepoBuckets(buckets);
};

const OVERVIEW_SENSORS_QUERY = gql`
  query OverviewSensorsQuery {
    workspaceOrError {
      ... on Workspace {
        id
        locationEntries {
          id
          locationOrLoadError {
            ... on RepositoryLocation {
              id
              name
              repositories {
                id
                name
                sensors {
                  id
                  name
                  description
                  sensorType
                  sensorState {
                    id
                    ...BasicInstigationStateFragment
                  }
                }
              }
            }
            ...PythonErrorFragment
          }
        }
      }
      ...PythonErrorFragment
    }
    unloadableInstigationStatesOrError(instigationType: SENSOR) {
      ... on InstigationStates {
        results {
          id
        }
      }
    }
    instance {
      id
      ...InstanceHealthFragment
    }
  }

  ${BASIC_INSTIGATION_STATE_FRAGMENT}
  ${PYTHON_ERROR_FRAGMENT}
  ${INSTANCE_HEALTH_FRAGMENT}
`;

const UNLOADABLE_SENSORS_QUERY = gql`
  query UnloadableSensorsQuery {
    unloadableInstigationStatesOrError(instigationType: SENSOR) {
      ... on InstigationStates {
        results {
          id
          ...InstigationStateFragment
        }
      }
      ...PythonErrorFragment
    }
  }

  ${INSTIGATION_STATE_FRAGMENT}
  ${PYTHON_ERROR_FRAGMENT}
`;
