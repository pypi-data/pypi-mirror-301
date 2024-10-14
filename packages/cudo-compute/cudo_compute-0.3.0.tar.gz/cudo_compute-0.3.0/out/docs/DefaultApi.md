# cudo_compute.DefaultApi

All URIs are relative to *https://rest.compute.cudo.org*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_billing_account_projects**](DefaultApi.md#list_billing_account_projects) | **GET** /v1/billing-accounts/{id}/projects | 
[**list_data_center_machine_type_prices**](DefaultApi.md#list_data_center_machine_type_prices) | **GET** /v1/data-centers/{dataCenterId}/machine-type-prices | 
[**search_resources**](DefaultApi.md#search_resources) | **GET** /v1/resources/search | 
[**track**](DefaultApi.md#track) | **POST** /v1/auth/track | 
[**update_vm_expire_time**](DefaultApi.md#update_vm_expire_time) | **POST** /v1/projects/{projectId}/vm/{id}/expire-time | 


# **list_billing_account_projects**
> ListBillingAccountProjectsResponse list_billing_account_projects(id)



### Example
```python
from __future__ import print_function
import time
import cudo_compute
from cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cudo_compute.DefaultApi()
id = 'id_example' # str | string page_token = 2;  int32 page_size = 3;

try:
    api_response = api_instance.list_billing_account_projects(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->list_billing_account_projects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| string page_token &#x3D; 2;  int32 page_size &#x3D; 3; | 

### Return type

[**ListBillingAccountProjectsResponse**](ListBillingAccountProjectsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_data_center_machine_type_prices**
> ListDataCenterMachineTypePricesResponse list_data_center_machine_type_prices(data_center_id)



### Example
```python
from __future__ import print_function
import time
import cudo_compute
from cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cudo_compute.DefaultApi()
data_center_id = 'data_center_id_example' # str | 

try:
    api_response = api_instance.list_data_center_machine_type_prices(data_center_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->list_data_center_machine_type_prices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_center_id** | **str**|  | 

### Return type

[**ListDataCenterMachineTypePricesResponse**](ListDataCenterMachineTypePricesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_resources**
> SearchResourcesResponse search_resources(query)



### Example
```python
from __future__ import print_function
import time
import cudo_compute
from cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cudo_compute.DefaultApi()
query = 'query_example' # str | 

try:
    api_response = api_instance.search_resources(query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->search_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 

### Return type

[**SearchResourcesResponse**](SearchResourcesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **track**
> object track(track_body)



### Example
```python
from __future__ import print_function
import time
import cudo_compute
from cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cudo_compute.DefaultApi()
track_body = cudo_compute.TrackRequest() # TrackRequest | 

try:
    api_response = api_instance.track(track_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->track: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **track_body** | [**TrackRequest**](TrackRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_vm_expire_time**
> UpdateVMExpireTimeResponse update_vm_expire_time(project_id, id, update_vm_expire_time_body)



### Example
```python
from __future__ import print_function
import time
import cudo_compute
from cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cudo_compute.DefaultApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 
update_vm_expire_time_body = cudo_compute.UpdateVMExpireTimeBody() # UpdateVMExpireTimeBody | 

try:
    api_response = api_instance.update_vm_expire_time(project_id, id, update_vm_expire_time_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->update_vm_expire_time: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 
 **update_vm_expire_time_body** | [**UpdateVMExpireTimeBody**](UpdateVMExpireTimeBody.md)|  | 

### Return type

[**UpdateVMExpireTimeResponse**](UpdateVMExpireTimeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

