import {Button, Icon, Menu, MenuItem, Popover, Spinner, Tooltip} from '@dagster-io/ui';
import * as React from 'react';

import {usePermissionsForLocation} from '../app/Permissions';
import {AssetKeyInput} from '../graphql/types';
import {MenuLink} from '../ui/MenuLink';
import {RepoAddress} from '../workspace/types';
import {workspacePathFromAddress} from '../workspace/workspacePath';

import {useMaterializationAction} from './LaunchAssetExecutionButton';
import {assetDetailsPathForKey} from './assetDetailsPathForKey';
import {AssetTableDefinitionFragment} from './types/AssetTableFragment.types';

interface Props {
  path: string[];
  definition: AssetTableDefinitionFragment | null;
  repoAddress: RepoAddress | null;
  onWipe?: (assets: AssetKeyInput[]) => void;
}

export const AssetActionMenu: React.FC<Props> = (props) => {
  const {repoAddress, path, definition, onWipe} = props;
  const {
    permissions: {canWipeAssets, canLaunchPipelineExecution},
  } = usePermissionsForLocation(repoAddress?.location);

  const {onClick, loading, launchpadElement} = useMaterializationAction();

  return (
    <>
      <Popover
        position="bottom-right"
        content={
          <Menu>
            <Tooltip
              content={
                !canLaunchPipelineExecution
                  ? 'You do not have permission to materialize assets'
                  : 'Shift+click to add configuration'
              }
              placement="left"
              display="block"
              useDisabledButtonTooltipFix
            >
              <MenuItem
                text="Materializar"
                icon={loading ? <Spinner purpose="body-text" /> : 'materialization'}
                disabled={!canLaunchPipelineExecution || loading}
                onClick={(e) => onClick([{path}], e)}
              />
            </Tooltip>
            <MenuLink
              text="Mostrar grupo"
              to={
                repoAddress && definition?.groupName
                  ? workspacePathFromAddress(repoAddress, `/asset-groups/${definition.groupName}`)
                  : ''
              }
              disabled={!definition}
              icon="asset_group"
            />
            <MenuLink
              text="Ver os vizinhos"
              to={assetDetailsPathForKey({path}, {view: 'lineage', lineageScope: 'neighbors'})}
              disabled={!definition}
              icon="graph_neighbors"
            />
            <MenuLink
              text="Ver montante de ativos"
              to={assetDetailsPathForKey({path}, {view: 'lineage', lineageScope: 'upstream'})}
              disabled={!definition}
              icon="graph_upstream"
            />
            <MenuLink
              text="Ver jusante de ativos"
              to={assetDetailsPathForKey({path}, {view: 'lineage', lineageScope: 'downstream'})}
              disabled={!definition}
              icon="graph_downstream"
            />
            <MenuItem
              text="Limpar materialização"
              icon="delete"
              disabled={!onWipe || !canWipeAssets}
              intent="danger"
              onClick={() => canWipeAssets && onWipe && onWipe([{path}])}
            />
          </Menu>
        }
      >
        <Button icon={<Icon name="expand_more" />} />
      </Popover>
      {launchpadElement}
    </>
  );
};
