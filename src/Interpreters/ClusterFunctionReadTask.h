#pragma once
#include <Core/Types.h>
#include <Storages/ObjectStorage/IObjectIterator.h>
#include "Storages/ObjectStorage/DataLakes/DataLakeObjectMetadata.h"


namespace DB
{
class ReadBuffer;
class WriteBuffer;

struct ClusterFunctionReadTask
{
    ClusterFunctionReadTask() = default;
    explicit ClusterFunctionReadTask(const std::string & path_) : path(path_) {}
    explicit ClusterFunctionReadTask(ObjectInfoPtr object);

    String path;
    DataLakeObjectMetadata data_lake_metadata;

    ObjectInfoPtr getObjectInfo() const
    {
        auto object = std::make_shared<ObjectInfo>(path);
        object->data_lake_metadata = data_lake_metadata;
        return object;
    }

    void serialize(WriteBuffer & out, size_t protocol_version) const;
    void deserialize(ReadBuffer & in);
};

using ClusterFunctionReadTaskPtr = std::shared_ptr<ClusterFunctionReadTask>;
using ClusterFunctionReadTaskCallback = std::function<ClusterFunctionReadTaskPtr()>;

}
