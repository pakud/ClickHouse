#include <Interpreters/ClusterFunctionReadTask.h>
#include <Interpreters/SetSerialization.h>
#include <Interpreters/Context.h>
#include <Core/ProtocolDefines.h>
#include <IO/WriteHelpers.h>
#include <IO/ReadHelpers.h>
#include "Interpreters/ActionsDAG.h"
#include "Storages/ObjectStorage/StorageObjectStorageSource.h"

namespace DB
{
namespace ErrorCodes
{
    extern const int UNKNOWN_PROTOCOL;
}
ClusterFunctionReadTask::ClusterFunctionReadTask(ObjectInfoPtr object)
{
    if (object->data_lake_metadata.has_value())
        data_lake_metadata = object->data_lake_metadata.value();

    if (auto archive_object_info = std::dynamic_pointer_cast<StorageObjectStorageSource::ArchiveIterator::ObjectInfoInArchive>(object);
        archive_object_info != nullptr)
    {
        path = archive_object_info->getPathToArchive();
    }
    else
    {
        path = object->getPath();
    }
}

void ClusterFunctionReadTask::serialize(WriteBuffer & out, size_t protocol_version) const
{
    writeVarUInt(protocol_version, out);
    writeStringBinary(path, out);

    if (protocol_version >= DBMS_CLUSTER_PROCESSING_PROTOCOL_VERSION_WITH_DATA_LAKE_METADATA)
    {
        SerializedSetsRegistry registry;
        data_lake_metadata.transform->serialize(out, registry);
    }
}

void ClusterFunctionReadTask::deserialize(ReadBuffer & in)
{
    size_t protocol_version = 0;
    readVarUInt(protocol_version, in);
    if (protocol_version < DBMS_CLUSTER_INITIAL_PROCESSING_PROTOCOL_VERSION
        || protocol_version > DBMS_CLUSTER_PROCESSING_PROTOCOL_VERSION)
    {
        throw Exception(
            ErrorCodes::UNKNOWN_PROTOCOL, "Supported protocol versions are in range [{}, {}], got: {}",
            DBMS_CLUSTER_INITIAL_PROCESSING_PROTOCOL_VERSION, DBMS_CLUSTER_PROCESSING_PROTOCOL_VERSION,
            protocol_version);
    }

    readStringBinary(path, in);
    if (protocol_version >= DBMS_CLUSTER_PROCESSING_PROTOCOL_VERSION_WITH_DATA_LAKE_METADATA)
    {
        DeserializedSetsRegistry registry;
        ActionsDAG::deserialize(in, registry, Context::getGlobalContextInstance());
    }
}

}
